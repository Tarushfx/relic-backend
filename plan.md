# Logger
## Requirement: 

Create an app to create your own table/fields and maintain all logs

Stack:
- Django
- PostgreSQL
- React Native


## DB Design
User
LogDefinition
LogEntry
Profile: preferences
Invitations
SystemPulse
Dashboard settings


## Plan

### Phase 1: Set up backend and design DB and API
### Phase 2: Front end
### Phase 3: Move to Phone
### Phase 4: AI integration

#### V1 
- Push releases to users
- Make auth easy
- Widgets 
- Create log table: add entry, maintain history
- Request throttling
- Idempotency
- notification and reminders

#### V2
- email verifification and how to make users verify if not verified
- Async storage for backend down - offline drafting
- Import and export
- add column(edit is rate limited)
- Table type summary, simple eval or AI


### Auth
v1
- simple user id and password
- check for invite table
    invitation pattern
- let user create account
- how to save password for user in google saved passwords
- jwt with 30 day refresh token
    Refresh token pattern: 2 token strategy: access token and refresh token
    Future scope increase the token duration to 24 hours for offline drafting
- keep time zones in mind: will cause the jwt to expire early

