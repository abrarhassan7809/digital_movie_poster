import os


def get_all_groups(IMAGEDIR):
    groups = []
    if os.path.exists(IMAGEDIR):
        groups = [name for name in os.listdir(IMAGEDIR) if os.path.isdir(os.path.join(IMAGEDIR, name))]
    return groups
