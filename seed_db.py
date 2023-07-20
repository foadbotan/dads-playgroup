from models import User, Event


def seed_db(db):
    db.drop_all()
    db.create_all()

    user1 = User(name="Bob", email="bob@example.com", password="password")
    user2 = User(name="John", email="john@example.com", password="password")
    me = User(name="Foad", email="1", password="1", is_admin=True)
    admin1 = User(
        name="Admin Harry",
        email="harry@example.com",
        password="password",
        is_admin=True,
    )
    admin2 = User(
        name="Admin David",
        email="david@example.com",
        password="password",
        is_admin=True,
    )

    event1 = admin1.create_event(
        name="Wednesdays playgroup - Haig Park",
        date="2023-07-26",
        time="9:00:00",
        description="This is the first event",
        location="123 Main St, Springfield, USA",
        image_url="https://images.unsplash.com/photo-1606733894347-7cb201dc810b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
    )
    event2 = admin1.create_event(
        name="Tuesday playgroup - Library",
        date="2023-07-25",
        time="9:30:00",
        description="This is the second event",
        location="123 Main St, Springfield, USA",
        image_url="https://images.unsplash.com/photo-1680178776508-41a276595b0f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
    )
    event3 = admin1.create_event(
        name="Friday playgroup - Zoo",
        date="2023-07-28",
        time="12:00:00",
        description="This is the third event",
        location="123 Main St, Springfield, USA",
        image_url="https://plus.unsplash.com/premium_photo-1664355811228-3baa53f4b179?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
    )
    event4 = admin1.create_event(
        name="Wednesday playgroup - Hike Mount Ainslie",
        date="2023-07-19",
        time="18:00:00",
        description="This is the fourth event",
        location="123 Main St, Springfield, USA",
        image_url="https://images.unsplash.com/photo-1627735410283-01be5efae8e1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
    )

    event1.attendees.extend([user1, user2])
    event2.attendees.extend([admin2, user2])
    event3.attendees.append(user1)

    db.session.add_all([event1, event2, event3, event4])

    db.session.commit()
    print("Database seeded!")
