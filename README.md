# Nittany Business (CMPSC431W Project)

---

## Progress
| Date       | Progress                                     |
|------------|----------------------------------------------|
| 23-Mar-2025| [Implemented User Authentication System](#user-authentication) |

## Tech Stack
- Python
- Flask
- SQLite
- HTML
- TailwindCSS

## User Authentication
- Implemented `Login` and `SignUp` feature.
- Users can use their credentials to login. If login fails, user is redirected back to the `Login page`, else is redirected to the `Homepage`.
- User can create accounts as well. If use does not exist, an account is successfully created, else an error is thrown and the user is redirected back to the `Sign Up` page.
- All passwords are hashed and stored in the database using the `sha256` algorithm.

## Color Palette
*All colors sourced from [coolors.com](https://coolors.co)*

- `#1C1C1C` - Eerie Black
- `#757575` - Gray
- `#DADDD8` - Platinum
- `#ECEBE4` - Alabaster
- `#EEF0F2` - Anti-flash White
- `#FAFAFF` - Ghost White
- `#669D31` - Asparagus
