def is_admin(user):
    return bool(user) and user.get("role") == "admin"


def require_admin(user):
    if not is_admin(user):
        raise PermissionError("Admin access required.")