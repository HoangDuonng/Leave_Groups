try:
    import tkinter as tk
    from tkinter import messagebox
except ModuleNotFoundError:
    tk = None
    messagebox = None

from telethon import utils
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogFiltersRequest

# Enter your API ID as a number, without quotes. Example: api_id = 123456
api_id = YOUR_API_ID_HERE

# Enter your API hash as text, keep the quotes.
api_hash = "YOUR_API_HASH_HERE"

# Telegram folder name to scan for groups, keep the quotes.
FOLDER_NAME = "YOUR_TELEGRAM_FOLDER_NAME_HERE"

# Local session file name. Do not push the .session file to Git.
client = TelegramClient("YOUR_SESSION_NAME_HERE", api_id, api_hash)


def get_folder_title(dialog_filter):
    title = getattr(dialog_filter, "title", "")
    return getattr(title, "text", str(title))


def get_peer_id(peer):
    return utils.get_peer_id(peer)


def find_folder(filters, folder_name):
    filters = get_dialog_filters(filters)

    return next(
        (
            dialog_filter
            for dialog_filter in filters
            if get_folder_title(dialog_filter).casefold() == folder_name.casefold()
        ),
        None,
    )


def get_dialog_filters(filters):
    return getattr(filters, "filters", filters)


def is_dialog_in_folder(dialog, dialog_filter, include_ids, exclude_ids):
    current_peer_id = get_peer_id(dialog.entity)

    if current_peer_id in exclude_ids:
        return False

    if current_peer_id in include_ids:
        return True

    return bool(getattr(dialog_filter, "groups", False) and dialog.is_group)


def get_groups_from_folder(folder_name):
    filters = client(GetDialogFiltersRequest())
    dialog_filters = get_dialog_filters(filters)
    target_filter = find_folder(dialog_filters, folder_name)

    if target_filter is None:
        available_folders = [
            get_folder_title(dialog_filter)
            for dialog_filter in dialog_filters
            if get_folder_title(dialog_filter)
        ]
        raise ValueError(
            f"Không tìm thấy folder '{folder_name}'. "
            f"Folder hiện có: {', '.join(available_folders) or 'không có'}"
        )

    include_ids = {
        get_peer_id(peer)
        for peer in [
            *getattr(target_filter, "include_peers", []),
            *getattr(target_filter, "pinned_peers", []),
        ]
    }
    exclude_ids = {
        get_peer_id(peer)
        for peer in getattr(target_filter, "exclude_peers", [])
    }

    groups = []
    for dialog in client.iter_dialogs():
        if dialog.is_group and is_dialog_in_folder(
            dialog,
            target_filter,
            include_ids,
            exclude_ids,
        ):
            groups.append(dialog)

    return groups


def build_gui(groups):
    root = tk.Tk()
    root.title(f"Telegram Group Manager - {FOLDER_NAME}")
    root.geometry("500x600")

    checked_groups = []

    tk.Label(root, text=f"Tick group muốn OUT trong {FOLDER_NAME}:", font=("Arial", 12)).pack()

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    if not groups:
        tk.Label(scroll_frame, text=f"Không có group nào trong {FOLDER_NAME}.").pack(anchor="w")

    for group in groups:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(scroll_frame, text=group.name, variable=var)
        checkbox.pack(anchor="w")
        checked_groups.append((var, group))

    def select_all_groups():
        for var, _ in checked_groups:
            var.set(True)

    def clear_selection():
        for var, _ in checked_groups:
            var.set(False)

    def leave_selected():
        selected = [group for var, group in checked_groups if var.get()]

        if not selected:
            messagebox.showinfo("Info", "Chưa chọn group nào")
            return

        confirm = messagebox.askyesno(
            "Confirm",
            f"Bạn chắc muốn OUT {len(selected)} group?",
        )

        if not confirm:
            return

        errors = leave_groups(selected)

        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return

        messagebox.showinfo("Done", "Đã out xong!")
        root.destroy()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="SELECT ALL", command=select_all_groups).pack(side="left", padx=10)

    tk.Button(button_frame, text="CLEAR", command=clear_selection).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="OUT SELECTED",
        command=leave_selected,
        bg="red",
        fg="white",
    ).pack(side="left", padx=10)

    tk.Button(button_frame, text="CANCEL", command=root.destroy).pack(side="left", padx=10)

    root.mainloop()


def show_groups_in_terminal(groups):
    print(f"\n===== GROUP TRONG {FOLDER_NAME} =====\n")

    if not groups:
        print(f"Không có group nào trong {FOLDER_NAME}.")
        return

    for index, group in enumerate(groups, 1):
        print(f"{index:02d}. {group.name}")

    print("\nNhập số group muốn OUT, ví dụ: 1,3,5 hoặc 2-4")
    print("Nhập all để chọn tất cả group trong folder.")
    print("Nhập q rồi Enter để hủy.")

    selected_text = input(">> ").strip()
    if selected_text.casefold() in {"q", "quit", "cancel", "huy", "hủy"}:
        print("Đã hủy, không out group nào.")
        return

    try:
        selected_indexes = parse_selection(selected_text, len(groups))
    except ValueError:
        print("Input không hợp lệ, đã hủy.")
        return

    if not selected_indexes:
        print("Không chọn group hợp lệ, đã hủy.")
        return

    selected_groups = [groups[index - 1] for index in selected_indexes]

    print("\nSẼ OUT:")
    for group in selected_groups:
        print("-", group.name)

    confirm = input("\nGõ YES để xác nhận, Enter/q để hủy: ").strip()
    if confirm != "YES":
        print("Đã hủy, không out group nào.")
        return

    leave_groups(selected_groups)


def parse_selection(selected_text, max_index):
    if selected_text.casefold() in {"all", "a", "*"}:
        return list(range(1, max_index + 1))

    indexes = set()

    for part in selected_text.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start = int(start_text.strip())
            end = int(end_text.strip())
            if start > end:
                start, end = end, start
            indexes.update(range(start, end + 1))
        else:
            indexes.add(int(part))

    return [index for index in sorted(indexes) if 1 <= index <= max_index]


def leave_groups(groups):
    errors = []

    for group in groups:
        try:
            print("Leaving:", group.name)
            client.delete_dialog(group.entity)
        except Exception as error:
            errors.append(f"{group.name}: {error}")

    if errors:
        print("\nCó lỗi:")
        for error in errors:
            print("-", error)
        return errors

    print("\nDONE")
    return []


with client:
    try:
        folder_groups = get_groups_from_folder(FOLDER_NAME)
    except ValueError as error:
        if messagebox is None:
            print(f"Error: {error}")
        else:
            messagebox.showerror("Error", str(error))
    else:
        if tk is None:
            show_groups_in_terminal(folder_groups)
        else:
            build_gui(folder_groups)
