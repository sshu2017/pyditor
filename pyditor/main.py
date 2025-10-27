import tkinter as tk
from pyditor.menu import create_menu
from pyditor.runner import run_code
from pyditor.utils import get_monitors_xrandr
import threading
import re
import keyword
import builtins


def main():
    def on_click():
        # get the code from the existing text widget
        source = text_widget.get("1.0", tk.END)

        # clear and show a running status
        output_text_widget.delete("1.0", tk.END)
        output_text_widget.insert("1.0", "Running ...")

        def worker():
            stdout, stderr, rc = run_code(source)

            # Update the GUI on the main thread
            def write_result():
                output_text_widget.delete("1.0", tk.END)
                # Insert stdout in green
                if rc == 0:
                    text_out = stdout or ("no output")
                    output_text_widget.insert("1.0", text_out, "stdout")
                elif rc == 1:
                    output_text_widget.insert("1.0", "--- STDOUT ---\n", "stdout")
                    output_text_widget.insert(
                        tk.END, stdout or "(no stdout)\n", "stdout"
                    )
                    output_text_widget.insert(tk.END, "--- STDERR ---\n", "stderr")
                    output_text_widget.insert(
                        tk.END, stderr or "(no stderr)\n", "stderr"
                    )
                elif rc == -1:
                    output_text_widget.insert(tk.END, "--- STDERR ---\n", "stderr")
                    output_text_widget.insert(
                        tk.END, stderr or "(no stderr)\n", "stderr"
                    )

            root.after(0, write_result)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    root = tk.Tk()
    root.title("Pyditor")

    # Start the window maximized
    def center_window_xrandr(width_ratio=0.5, height_ratio=0.8):
        root.update_idletasks()

        monitors = get_monitors_xrandr()

        if not monitors:
            # Fallback to standard tkinter method
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            monitor = {"name": "Primary", "x": 0, "y": 0, "width": screen_width, "height": screen_height}
        else:
            # Get mouse position
            mouse_x = root.winfo_pointerx()
            mouse_y = root.winfo_pointery()

            # Find monitor containing mouse
            monitor = None
            for m in monitors:
                if (
                    m["x"] <= mouse_x < m["x"] + m["width"]
                    and m["y"] <= mouse_y < m["y"] + m["height"]
                ):
                    monitor = m
                    break

            # Fallback to primary or first monitor
            if monitor is None:
                monitor = next(
                    (m for m in monitors if m.get("is_primary")), monitors[0]
                )

        print(
            f"Using monitor: {monitor['name']} ({monitor['width']}x{monitor['height']})"
        )

        # Calculate window size
        win_width = int(monitor["width"] * width_ratio)
        win_height = int(monitor["height"] * height_ratio)

        win_width = max(600, min(win_width, monitor["width"] - 100))
        win_height = max(400, min(win_height, monitor["height"] - 100))

        # Calculate position relative to monitor
        x = monitor["x"] + (monitor["width"] - win_width) // 2
        y = monitor["y"] + (monitor["height"] - win_height) // 2

        root.geometry(f"{win_width}x{win_height}+{x}+{y}")

    center_window_xrandr()

    # bring windown to front so it is not hidden behind other apps
    try:
        root.deiconify()
        root.lift()
        root.focus_force()
        # some platforms respect -topmost. toggle it briefly to ensure visibility
        root.attributes("-topmost", True)
        root.after(100, lambda: root.attributes("-topmost", False))
    except Exception:
        pass

    # Use cross-platform font with fallbacks
    import sys
    if sys.platform == "darwin":  # macOS
        default_font = ("Monaco", 18)
        btn_font_config = ("Monaco", 18, "bold")
    elif sys.platform == "win32":  # Windows
        default_font = ("Consolas", 14)
        btn_font_config = ("Consolas", 14, "bold")
    else:  # Linux/Unix
        default_font = ("DejaVu Sans Mono", 14)
        btn_font_config = ("DejaVu Sans Mono", 14, "bold")

    text_bg = "#dad9ce"
    text_fg = "#1A0909"

    text_widget = tk.Text(
        root,
        wrap=tk.WORD,
        height=12,
        font=default_font,
        bg=text_bg,
        fg=text_fg,
        insertbackground="#000000",
        insertwidth=4,
        insertontime=600,
        insertofftime=300,
        selectbackground="#e8b6a9",
        selectforeground="#000000",
    )

    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    placeholder_text = "type python codes here ..."
    text_widget.insert("1.0", placeholder_text)
    # tag placeholder and style it gray
    text_widget.tag_add("placeholder", "1.0", "end")
    text_widget.tag_configure("placeholder", foreground="#888888")

    # ---- syntax highlighting setup ---
    text_widget.tag_configure("py_keyword", foreground="#0000FF")
    text_widget.tag_configure("py_string", foreground="#B22222")
    text_widget.tag_configure("py_comment", foreground="#008000")
    text_widget.tag_configure("py_number", foreground="#164000")
    text_widget.tag_configure("py_builtin", foreground="#6A5ACD")

    # precompile regex patterns
    kw_regex = re.compile(r"\b(" + r"|".join(map(re.escape, keyword.kwlist)) + r")\b")
    str_regex = re.compile(
        r"('''.*?'''|\"\"\".*?\*\*\*|\'[^\n']*\'|\"[^\n\"]*\")", re.S
    )
    comment_regex = re.compile(r"#.*")
    number_regex = re.compile(r"\b\d+(?:\.\d+)?\b")
    builtin_names = [b for b in dir(builtins) if not b.startswith("_")]
    builtin_regex = re.compile(
        r"\b(" + r"|".join(map(re.escape, builtin_names)) + r")\b"
    )

    highlight_job = None

    def do_highlight():
        # remove previous syntax tags but keep placeholder tag untouched
        for tag in ["py_keyword", "py_string", "py_comment", "py_number", "py_builtin"]:
            text_widget.tag_remove(tag, "1.0", tk.END)

        content = text_widget.get("1.0", "end-1c")
        if not content or content == placeholder_text:
            return

        # apply comment first so it's not re-colored by keywords inside
        for m in comment_regex.finditer(content):
            start, end = m.span()
            text_widget.tag_add("py_comment", f"1.0 + {start}c", f"1.0 + {end}c")

        for m in kw_regex.finditer(content):
            start, end = m.span()
            text_widget.tag_add("py_keyword", f"1.0 + {start}c", f"1.0 + {end}c")

        for m in str_regex.finditer(content):
            start, end = m.span()
            text_widget.tag_add("py_string", f"1.0 + {start}c", f"1.0 + {end}c")

        for m in number_regex.finditer(content):
            start, end = m.span()
            text_widget.tag_add("py_number", f"1.0 + {start}c", f"1.0 + {end}c")

        for m in builtin_regex.finditer(content):
            start, end = m.span()
            text_widget.tag_add("py_builtin", f"1.0 + {start}c", f"1.0 + {end}c")

    def schedule_highlight(event=None):
        nonlocal highlight_job
        if highlight_job:
            text_widget.after_cancel(highlight_job)
            highlight_job = None
        highlight_job = text_widget.after(250, do_highlight)

    # bind key and paste events to trigger highlighting
    text_widget.bind("<KeyRelease>", schedule_highlight)
    text_widget.bind("<<Paste>>", schedule_highlight)

    def clear_placeholder(event):
        if text_widget.get("1.0", "end-1c") == placeholder_text:
            text_widget.delete("1.0", tk.END)
            text_widget.tag_remove("placeholder", "1.0", tk.END)
            schedule_highlight()

    text_widget.bind("<FocusIn>", clear_placeholder)

    menu_handler = create_menu(root)
    menu_handler.set_text_widget(text_widget)

    ## create run button
    try:
        submit_btn = tk.Button(
            root,
            text="Run",
            command=on_click,
            font=btn_font_config,
            bg="#E0620E",
            fg="#FFFFFF",
            activebackground="gray",
            bd=0,
            relief=tk.RAISED,
            height=1,
            width=18,
        )
    except Exception:
        submit_btn = tk.Button(
            root, text="Run", command=on_click, font=btn_font_config, height=1, width=18
        )

    submit_btn.pack(padx=0, pady=0, ipadx=6, ipady=12)

    output_text_widget = tk.Text(
        root,
        #  height=18,
        wrap=tk.WORD,
        font=default_font,
        bg=text_bg,
        fg=text_fg,
        insertbackground="#000000",
        insertwidth=4,
        insertontime=600,
        insertofftime=300,
        selectbackground="#cfe8a9",
        selectforeground="#000000",
    )

    output_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 10))

    output_placeholder = "Output area ..."
    output_text_widget.insert("1.0", output_placeholder)
    output_text_widget.tag_add("placeholder", "1.0", "end")
    output_text_widget.tag_configure("placeholder", foreground="#888888")
    output_text_widget.tag_configure("stdout", foreground="#006400")  # dark green
    output_text_widget.tag_configure("stderr", foreground="#B22222")  # firebrick red

    root.mainloop()


if __name__ == "__main__":
    main()
