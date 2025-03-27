def generate_reservation_email_body(payload):
    return f"You have a reservation for book {payload.get('book_group')}. It is now available. You can accept: {payload.get("links").get("accept")}, skip: {payload.get("links").get("skip")} or cancel: {payload.get("links").get("cancel")}"
