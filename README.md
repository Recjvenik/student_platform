# Student Training & Job Platform - Django POC

A mobile-first Proof-of-Concept (POC) for a platform that trains graduating students and connects them to jobs. This platform collects detailed student data through a multi-step registration system and provides authentication via Google OAuth or Mobile Number + OTP.

## Features

✅ **Authentication System**
- Google OAuth Sign-in (via django-allauth)
- Mobile Number + OTP Login (90-second expiry)
- Custom User model supporting both auth methods

✅ **Multi-Step Registration (8 Steps)**
1. Basic Information (Name, Gender, DOB, Location, Languages)
2. Education Details (Qualification, College, Scores, Experience)
3. Skills & Exposure (English proficiency, Computer skills, Typing speed)
4. Career Preferences (Job roles, Industries, Work type, Salary)
5. Availability & Constraints (Training time, Device access, Internet)
6. Behavioural Survey (Comfort levels, Career goals)
7. Training Information (Discovery source, Fee preference, Commitment)
8. Document Upload (Photo, Resume, ID proof, Marksheet)

✅ **Additional Features**
- AJAX-based step-wise form saving
- Progress indicator
- Mobile-first responsive design
- Minimalist 2-color UI (Blue #2563eb + White)
- Django Admin with CSV export
- Profile review before submission
- Dashboard after completion

## Tech Stack

- **Backend**: Django 5.2.8 (MVT Architecture)
- **Database**: SQLite (can be switched to MySQL)
- **Authentication**: Django-Allauth (Google OAuth)
- **Caching/OTP**: In-memory cache (can use Redis)
- **Frontend**: HTML5, CSS3, JavaScript, jQuery
- **File Upload**: Django FileField/ImageField

## Project Structure

```
student_platform/
├── accounts/                   # Authentication app
│   ├── models.py              # User, OTPLog models
│   ├── views.py               # Login, OTP views
│   ├── admin.py               # Admin configuration
│   └── urls.py
├── students/                   # Student profile app
│   ├── models.py              # StudentProfile, Experience models
│   ├── views.py               # Multi-step form views
│   ├── admin.py               # Admin with CSV export
│   └── urls.py
├── config/                     # Project settings
│   ├── settings.py            # Django settings
│   └── urls.py                # Main URL routing
├── templates/
│   ├── base.html              # Base template
│   ├── home.html              # Landing page
│   ├── accounts/              # Authentication templates
│   └── students/              # Registration step templates
├── static/
│   ├── css/style.css          # Minimalist mobile-first CSS
│   └── js/main.js             # Common JavaScript utilities
├── media/                      # User-uploaded files
├── manage.py
└── db.sqlite3
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Step 1: Install Dependencies

```bash
pip install django django-allauth redis pillow --break-system-packages
```

### Step 2: Configure Google OAuth (Optional)

If you want to test Google Sign-in:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
6. Update `config/settings.py`:
   ```python
   SOCIALACCOUNT_PROVIDERS = {
       'google': {
           'APP': {
               'client_id': 'YOUR_CLIENT_ID',
               'secret': 'YOUR_SECRET',
           }
       }
   }
   ```

### Step 3: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 4: Run the Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Usage

### For Students

1. **Sign Up**: Visit the home page and choose sign-in method
   - **Mobile OTP**: Enter 10-digit mobile, check console for OTP
   - **Google**: Sign in with Google account

2. **Complete Profile**: Fill out the 8-step registration form
   - Progress is auto-saved at each step
   - Navigate forward/backward between steps
   - Review all information before final submission

3. **Dashboard**: After submission, view your profile summary

### For Admins

1. **Access Admin Panel**: http://127.0.0.1:8000/admin/
2. **View Students**: See all registered student profiles
3. **Export Data**: Select students and use "Export Selected as CSV" action
4. **Search/Filter**: Find students by name, email, phone, college

## Database Models

### User (Custom User Model)
- email, mobile, name
- auth_type (google/otp)
- google_uid, profile_picture
- Timestamps

### OTPLog
- mobile, otp, expiry
- verified, verified_at
- Tracks all OTP generation/verification

### StudentProfile
- One-to-One with User
- All 8 sections of data (60+ fields)
- Progress tracking (step_completed)
- Document uploads
- Timestamps

### Experience
- ForeignKey to StudentProfile
- company_name, role, duration, description
- For internships/work experience

## API Endpoints

### Authentication
- `GET /` - Home page
- `GET /login/` - Login options
- `GET|POST /login/mobile/` - Mobile login (sends OTP)
- `GET|POST /verify-otp/` - Verify OTP
- `GET /accounts/google/login/` - Google OAuth

### Profile Registration
- `GET /profile/start/` - Start/continue registration
- `GET /profile/step/<n>/` - Individual step (1-8)
- `POST /profile/save-step/` - AJAX save endpoint
- `GET /profile/review/` - Review before submit
- `POST /profile/submit/` - Final submission
- `POST /profile/upload-documents/` - Document upload

### Dashboard
- `GET /dashboard/` - User dashboard

## Admin Features

- View all student profiles with search/filter
- Export selected profiles to CSV
- View full profile details including documents
- Track registration progress
- View OTP logs for debugging

## Design Philosophy

### Mobile-First
- Max-width: 500px on mobile, 600px on tablet+
- Touch-friendly buttons and inputs
- Responsive forms and layouts

### Minimalist UI
- 2 colors: Primary Blue (#2563eb), White background
- No heavy animations or shadows
- Clean card-based design
- Simple typography

### Performance
- AJAX saves reduce page loads
- Lightweight CSS (no frameworks)
- Minimal JavaScript dependencies (jQuery only)

## OTP System (POC)

For this POC, OTPs are printed to console instead of sent via SMS:

```python
# When user requests OTP, check console output:
==================================================
OTP for 9876543210: 123456
Valid for 90 seconds
==================================================
```

**Production Setup**: Replace console print with SMS gateway (Twilio, AWS SNS, etc.)

## Redis Configuration (Optional)

To use Redis for OTP caching instead of in-memory cache:

1. Install Redis: `sudo apt-get install redis-server`
2. Start Redis: `redis-server`
3. Update `config/settings.py`:
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

## MySQL Configuration (Optional)

To switch from SQLite to MySQL:

1. Install: `pip install mysqlclient`
2. Create database: `CREATE DATABASE student_platform;`
3. Update `config/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'student_platform',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
4. Run migrations: `python manage.py migrate`

## Testing the Platform

1. **Test Mobile OTP Login**:
   - Go to /login/mobile/
   - Enter: 9876543210
   - Check console for OTP
   - Enter OTP in verification page

2. **Test Registration Flow**:
   - Complete all 8 steps
   - Test form validation
   - Test previous/next navigation
   - Review before submission

3. **Test Admin Panel**:
   - Login to /admin/
   - View student profiles
   - Export to CSV
   - Search functionality

## Troubleshooting

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### Issue: OTP not working
**Solution**: Check console output for OTP, ensure 90 seconds haven't passed

### Issue: Google OAuth errors
**Solution**: Verify client ID/secret, check authorized redirect URIs

### Issue: File uploads failing
**Solution**: Ensure `media/` directory exists and has write permissions

## Future Enhancements

- SMS gateway integration for real OTPs
- Email notifications
- Job matching algorithm
- Training course management
- Payment integration
- Advanced reporting and analytics
- Mobile app (React Native)

## License

This is a POC project for educational purposes.

## Contact

For questions or support, please contact the development team.
