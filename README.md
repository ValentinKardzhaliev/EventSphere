# EventSphere Documentation

## Introduction

EventSphere is a web application designed to allow users to create, manage, and purchase tickets for events. Users can create events, manage their events, buy tickets for events, manage their purchased tickets, and more.

The website is deployed and accessible at [valentinkardzhaliev.pythonanywhere.com](https://valentinkardzhaliev.pythonanywhere.com/).

## Features

### User Authentication and Management

- Users can register and create an account using a username, email, and password.
- Upon registration, users are assigned a default profile picture and starting balance.
- Users can log in and log out of their accounts.
- After logging in, users can add money to their balance or change their profile picture.
- User authentication is handled using Django's built-in authentication system.
  
### Events Management

- Users can create events, specifying details such as title, description, location, date and time, venue, category, contact information, organizer, and image.
- Events are categorized into different categories such as Music, Nightlife, Performing & Visual Arts, Holidays, Health, Hobbies, Business, and Food & Drink.
- Users can view details of events they have created.
- Only the creators of events can edit their own events.
- Events are displayed on the website's homepage.

### Ticket Management

- Users can purchase tickets for events.
- Regular and VIP ticket types are available.
- Users can view their purchased tickets.
- Users can see available tickets and prices before making a purchase.
- Users can see events they have liked.
- Users can refund their purchased tickets, provided that the request is made within a 24-hour window from the time of purchase.

### Searching

- Users can search for events by name using the search form.

## Future Plans

- Implement Stripe payment options for ticket purchases.

## Access Control

- All users have the same level of access and permissions.
- Only the creators of events can edit their own events.

## Testing

The website has been manually tested to ensure functionality and usability.

## Conclusion

EventSphere provides a convenient platform for users to create, manage, and participate in various events. With features for event creation, ticket purchase, and user management, it offers a comprehensive solution for event organization and attendance.
