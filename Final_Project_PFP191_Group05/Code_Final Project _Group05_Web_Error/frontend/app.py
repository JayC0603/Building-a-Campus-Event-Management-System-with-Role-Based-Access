"""
Flask web application for Campus Event Management System
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sys
import os
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from backend.main import CampusEventManager
    from backend.models.user import UserRole
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure you're running from the project root directory")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize the event manager
event_manager = CampusEventManager()


@app.route('/')
def index():
    """Trang chủ"""
    upcoming_events = event_manager.get_upcoming_events()[:6]  # Lấy 6 sự kiện sắp tới
    popular_events = event_manager.get_popular_events(6)  # Lấy 6 sự kiện phổ biến
    
    return render_template('index.html', 
                         upcoming_events=upcoming_events,
                         popular_events=popular_events)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Trang đăng nhập"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        result = event_manager.login(username, password)
        
        if result['success']:
            session['user_id'] = result['user'].user_id
            session['username'] = result['user'].username
            session['role'] = result['user'].role.value
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Đăng xuất"""
    event_manager.logout()
    session.clear()
    flash('Đã đăng xuất thành công', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    """Dashboard theo vai trò"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Load user info into event_manager
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
        stats = event_manager.get_dashboard_stats()
        
        if user.role == UserRole.ADMIN:
            return render_template('admin_dashboard.html', stats=stats, user=user)
        elif user.role == UserRole.ORGANIZER:
            return render_template('organizer_dashboard.html', stats=stats, user=user)
        else:
            return render_template('student_dashboard.html', stats=stats, user=user)
    
    return redirect(url_for('login'))


# ================== EVENT API ROUTES ==================

@app.route('/api/events', methods=['GET'])
def api_get_events():
    """API lấy danh sách sự kiện"""
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    filter_own = request.args.get('filter_own', 'false').lower() == 'true'
    
    # Load current user if logged in
    if 'user_id' in session:
        user = event_manager.auth_service.get_user_by_id(session['user_id'])
        if user:
            event_manager.auth_service.current_user = user
    
    if query or category or status:
        events = event_manager.search_events(query, category, status)
    else:
        events = event_manager.get_events(filter_own)
    
    # Convert events to dict
    events_data = []
    for event in events:
        organizer = event_manager.auth_service.get_user_by_id(event.organizer_id)
        event_dict = event.to_dict()
        event_dict['organizer_name'] = organizer.full_name if organizer else 'Unknown'
        events_data.append(event_dict)
    
    return jsonify(events_data)


@app.route('/api/events', methods=['POST'])
def api_create_event():
    """API tạo sự kiện mới"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    data = request.get_json()
    result = event_manager.create_event(
        title=data.get('title'),
        description=data.get('description'),
        event_date=data.get('event_date'),
        location=data.get('location'),
        max_capacity=int(data.get('max_capacity')),
        category=data.get('category', 'other')
    )
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@app.route('/api/events/<event_id>', methods=['PUT'])
def api_update_event(event_id):
    """API cập nhật sự kiện"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    data = request.get_json()
    
    # Remove None values
    update_data = {k: v for k, v in data.items() if v is not None}
    
    result = event_manager.update_event(event_id, **update_data)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@app.route('/api/events/<event_id>', methods=['DELETE'])
def api_delete_event(event_id):
    """API xóa sự kiện"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    result = event_manager.delete_event(event_id)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


# ================== REGISTRATION API ROUTES ==================

@app.route('/api/events/<event_id>/register', methods=['POST'])
def api_register_event(event_id):
    """API đăng ký tham gia sự kiện"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    result = event_manager.register_for_event(event_id)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@app.route('/api/events/<event_id>/unregister', methods=['POST'])
def api_unregister_event(event_id):
    """API hủy đăng ký sự kiện"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    data = request.get_json()
    reason = data.get('reason', '') if data else ''
    
    result = event_manager.cancel_registration(event_id, reason)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@app.route('/api/my-registrations')
def api_my_registrations():
    """API lấy đăng ký của user hiện tại"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    registrations = event_manager.get_user_registrations()
    
    # Convert to dict
    registrations_data = []
    for reg_data in registrations:
        event = reg_data['event']
        registration = reg_data['registration']
        
        registrations_data.append({
            'event': event.to_dict(),
            'registration': registration.to_dict()
        })
    
    return jsonify(registrations_data)


@app.route('/api/events/<event_id>/registrations')
def api_event_registrations(event_id):
    """API lấy danh sách đăng ký của một sự kiện"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    registrations = event_manager.get_event_registrations(event_id)
    
    # Convert to dict with user info
    registrations_data = []
    for registration in registrations:
        user_info = event_manager.auth_service.get_user_by_id(registration.user_id)
        reg_dict = registration.to_dict()
        reg_dict['user_name'] = user_info.full_name if user_info else 'Unknown'
        reg_dict['user_email'] = user_info.email if user_info else 'Unknown'
        registrations_data.append(reg_dict)
    
    return jsonify(registrations_data)


# ================== STATISTICS AND REPORTS ==================

@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    """API lấy thống kê dashboard"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
        stats = event_manager.get_dashboard_stats()
        return jsonify(stats)
    
    return jsonify({'success': False, 'message': 'User not found'}), 404


@app.route('/api/reports/events/export')
def api_export_events_report():
    """API xuất báo cáo sự kiện"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
        result = event_manager.export_events_report()
        return jsonify(result)
    
    return jsonify({'success': False, 'message': 'User not found'}), 404


@app.route('/api/reports/registrations/export')
def api_export_registrations_report():
    """API xuất báo cáo đăng ký"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
        result = event_manager.export_registrations_report()
        return jsonify(result)
    
    return jsonify({'success': False, 'message': 'User not found'}), 404


# ================== UTILITY ROUTES ==================

@app.route('/api/registrations/<registration_id>/attendance', methods=['POST'])
def api_mark_attendance(registration_id):
    """API đánh dấu tham gia/vắng mặt"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
    
    data = request.get_json()
    attended = data.get('attended', True)
    
    result = event_manager.registration_service.mark_attendance(registration_id, attended)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@app.route('/api/register', methods=['POST'])
def api_register_user():
    """API đăng ký user mới"""
    data = request.get_json()
    
    result = event_manager.register_user(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password'),
        role=data.get('role'),
        full_name=data.get('full_name', '')
    )
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


# ================== UTILITY ROUTES ==================

@app.route('/api/system/backup')
def api_system_backup():
    """API sao lưu hệ thống"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Chưa đăng nhập'}), 401
    
    # Load current user
    user = event_manager.auth_service.get_user_by_id(session['user_id'])
    if user:
        event_manager.auth_service.current_user = user
        result = event_manager.backup_system_data()
        return jsonify(result)
    
    return jsonify({'success': False, 'message': 'User not found'}), 404


@app.route('/api/system/info')
def api_system_info():
    """API lấy thông tin hệ thống"""
    info = event_manager.get_system_info()
    return jsonify(info)


# ================== ERROR HANDLERS ==================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# ================== TEMPLATE FILTERS ==================

@app.template_filter('datetime')
def datetime_filter(value):
    """Filter để format datetime"""
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return value


@app.template_filter('date')
def date_filter(value):
    """Filter để format date"""
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y')
    except:
        return value


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)