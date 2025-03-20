# -*- coding: utf-8 -*-
# Inventories occurrences of each chapter label in UsfmCleanup's source_dir.

def main(gui = None):
    import inventory_chapter_labels
    inventory_chapter_labels.inventory(gui, 'UsfmCleanup')

if __name__ == "__main__":
    main()
