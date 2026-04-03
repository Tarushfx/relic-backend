# API desgin

## Auth and Invitations
(internal)
POST /api/v1/auth/invite/
POST /api/v1/auth/validate/{id}/
POST /api/v1/auth/login/
POST /api/v1/auth/signup/
POST /api/v1/auth/refresh/
POST /api/v1/auth/logout/

## Profile
GET /api/v1/profile/
POST /api/v1/profile/


## Table Manipulation
GET /api/v1/logs/tables/
POST /api/v1/logs/tables/
GET /api/v1/logs/tables/{id}/
PUT /api/v1/logs/tables/{id}/
DELETE /api/v1/logs/tables/{id}/

## Logging
GET /api/v1/logs/entries/
POST /api/v1/logs/entries/
GET /api/v1/logs/entries/{id}/
PUT /api/v1/logs/entries/{id}/
DELETE /api/v1/logs/entries/{id}/

## Health
GET /api/v1/health/