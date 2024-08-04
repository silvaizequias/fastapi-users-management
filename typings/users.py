def one(user) -> dict:
    return {
        "id": str(user["_id"]),
        "createdAt": str(user["createdAt"]),
        "updatedAt": str(user["updatedAt"]),
        "active": bool(user["active"]),
        "role": user["role"],
        "image": user["image"],
        "email": user["email"],
        "phone": user["phone"],
        "secret": user["secret"],
        "account": user["account"]
    }


def many(users) -> list:
    return [one(user) for user in users]