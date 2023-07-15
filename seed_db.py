def seed_db(db):
    db.drop_all()
    db.create_all()

    user1 = User.create(name="Bob", email="bob@example.com", password="password")
    user2 = User.create(name="John", email="john@example.com", password="password")
    admin1 = User.create(
        name="Admin Harry",
        email="harry@example.com",
        password="password",
        is_admin=True,
    )
    admin2 = User.create(
        name="Admin David",
        email="david@example.com",
        password="password",
        is_admin=True,
    )

    event1 = admin1.create_event(
        name="Event 1",
        date="2021-09-01",
        description="This is the first event",
        location="123 Main St, Springfield, USA",
        is_public=False,
    )
    event2 = admin1.create_event(
        name="Event 2",
        date="2021-09-02",
        description="This is the second event",
        location="123 Main St, Springfield, USA",
    )
    event3 = admin1.create_event(
        name="Event 3",
        date="2021-09-03",
        description="This is the third event",
        location="123 Main St, Springfield, USA",
    )
    event4 = admin1.create_event(
        name="Event 4",
        date="2021-09-04",
        description="This is the fourth event",
        location="123 Main St, Springfield, USA",
    )

    event1.attendees.extend([user1, user2])
    event2.attendees.extend([admin2, user2])
    event3.attendees.append(user1)

    db.session.commit()
    print("Database seeded!")
