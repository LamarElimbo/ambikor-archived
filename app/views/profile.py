from flask import Blueprint, redirect, render_template, request, session, url_for
from .. import mongo
from app.models import Message
from app.views import _helpers
import datetime, os


profile_blueprint = Blueprint('profile', __name__)


################# PAGES ###################

@profile_blueprint.route('/profile', methods=['GET', 'POST'])
def profile_page():
    try:
        user = mongo.db.users.find_one({"email": session['user_email']})
        mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$set": {'profile.notifications.new_notifications': "no"}})
        return render_template('profile/profile_edit_form.html', 
        skeleton=_helpers.get_skeleton(),
        industry_slider=None)
    except:
        return render_template('errors/500.html')
    
@profile_blueprint.route('/profile/<username>')
def user_profile(username):
    try:
        return render_template('profile/profile_user.html', 
        skeleton=_helpers.get_skeleton(), 
        industry_slider='home/_industry_slider.html' if 'user_email' in session else None,
        user=mongo.db.users.find_one({"profile.username": username}))
    except:
        return render_template('errors/500.html')
    
@profile_blueprint.route('/profile/edit')
def user_profile_edit():
        return render_template('profile/profile_edit_form.html', 
        skeleton=_helpers.get_skeleton(),
        industry_slider=None)

@profile_blueprint.route('/notifications')
def notifications_page():
    try:
        if 'user_email' in session:
            mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$set": {'profile.notifications.new_notifications': 'no'}})
            skeleton = _helpers.get_skeleton()
            for notification in skeleton['user']['profile']['notifications']['notifications_list']:
                user_to_get = notification['service_provider'] if notification['service_provider'] != skeleton['user']['user_id'] else notification['service_requester']
                user = mongo.db.users.find_one({"user_id": user_to_get})
                notification['user'] = {
                    'id': user['user_id'] if user != None else 'ghost',
                    'name': user['profile']['name'] if user != None else 'ghost',
                    'username': user['profile']['username'] if user != None else 'ghost',
                    'profile_image': user['profile']['profile_image']['src'] if user != None else 'ghost'
                }
                message = mongo.db.messages.find_one({"message_id": notification['messages_id']})
                last_message = message['messages'][0]
            return render_template('profile/notifications.html', skeleton=skeleton, industry_slider='home/_industry_slider.html' if 'user_email' in session else None)
        else:
            return redirect(url_for('home.home_page'))
    except:
        return render_template('errors/500.html')

@profile_blueprint.route('/settings', methods=["GET", "POST"])
def settings_page():
        if 'user_email' in session:
            return render_template('account/settings.html',
                                   skeleton=_helpers.get_skeleton(),
                                    industry_slider='home/_industry_slider.html' if 'user_email' in session else None)
        return redirect(url_for('home.home_page'))
    
@profile_blueprint.route('/earnings')
def earnings_page():
    try:
        skeleton = _helpers.get_skeleton()
        earnings = { "potential_earnings": 0, "pending_earnings": 0, "available_to_payout": 0, "earnings_to_date": 0 }
        for notification in skeleton['user']['profile']['notifications']['notifications_list']:
            if notification['service_provider'] == skeleton['user']['user_id']:
                user_to_get = notification['service_provider'] if notification['service_provider'] != skeleton['user']['user_id'] else notification['service_requester']
                user = mongo.db.users.find_one({"user_id": user_to_get})
                notification['user'] = {
                    'id': user['user_id'] if user != None else 'ghost',
                    'name': user['profile']['name'] if user != None else 'ghost',
                    'username': user['profile']['username'] if user != None else 'ghost',
                    'profile_image': user['profile']['profile_image']['src'] if user != None else 'ghost'
                }
                message = mongo.db.messages.find_one({"message_id": notification['messages_id']})
                if type(message['service']) == dict:
                    notification['cost'] = int(message['service']['cost'].strip('$'))
                    cost = int(message['service']['cost'].strip('$'))
                    if notification['status']['requester_charge'] == 'true' and notification['status']['completion_confirmed'] == 'false':
                        service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
                        service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
                        completion_date = datetime.datetime.strptime(notification['completion_date'], '%Y-%m-%d').date()
                        if (completion_date - datetime.date.today()).days < 0:
                            notification['status']['current_status'] = 'completion_confirmed'
                            notification['status']['completion_confirmed'] = 'true'
                            for user in [service_provider, service_requester]:
                                mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'completion_confirmed', "profile.notifications.notifications_list.$.status.completion_confirmed": 'true'} })
                    try:
                        if notification['status']['current_status'] in ['acceptance_pending', 'accepted']:
                            earnings["potential_earnings"] += cost
                        if notification['status']['current_status'] in ['charge_processed', 'complete']:
                            earnings["pending_earnings"] += cost
                        if notification['status']['completion_confirmed'] == 'true' and notification['status']['payout_processed'] == 'false':
                            earnings["available_to_payout"] += cost
                        if notification['status']['payout_processed'] == 'true':
                            earnings["earnings_to_date"] += cost
                    except:
                        continue
        return render_template('profile/earnings.html', skeleton=skeleton, earnings=earnings, industry_slider='home/_industry_slider.html' if 'user_email' in session else None)
    except:
        return render_template('errors/500.html')
    

################# NOTIFICATIONS ###################

@profile_blueprint.route('/notifications_archive', methods=['POST'])
def notifications_archive():
    skeleton = _helpers.get_skeleton()
    for notification in skeleton['user']['profile']['notifications']['notifications_list']:
        user_to_get = notification['service_provider'] if notification['service_provider'] != skeleton['user']['user_id'] else notification['service_requester']
        user = mongo.db.users.find_one({"user_id": user_to_get})
        notification['user'] = {
            'id': user['user_id'] if user != None else 'ghost',
            'name': user['profile']['name'] if user != None else 'ghost',
            'username': user['profile']['username'] if user != None else 'ghost',
            'profile_image': user['profile']['profile_image']['src'] if user != None else 'ghost'
        }
    return render_template('profile/notifications_archive.html', skeleton=skeleton)
    
    
################# PROFILE EDITING ###################

@profile_blueprint.route('/username_validation', methods=['POST'])
def username_validation():
    user = mongo.db.users.find_one({"email": session['user_email']})
    character_validation = 'pass'
    for char in request.form['username']:
        if type(char) == int or char.isalpha() or char in ['_', '-', '+']:
            character_validation = 'pass'
        else:
            character_validation = 'fail'
            break
    return render_template('profile/username_verification.html',
                           has_username='yes' if user['profile']['username'] == request.form['username'] else 'no',
                           character_validation=character_validation,
                           username_exists='no' if mongo.db.users.find_one({"profile.username": request.form['username']}) == None else 'yes')


################# MESSAGING ###################

@profile_blueprint.route('/get_message', methods=['POST'])
def get_message():
    messages = mongo.db.messages.find_one({"message_id": request.form['message_id']})
    user = mongo.db.users.find_one({"email": session['user_email']})
    for notification in user['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['message_id']:
            service_provider = notification['service_provider']
            service_requester = notification['service_requester']
            service_name = notification['service']
    user_is_service_provider = 'true' if service_provider == user['user_id'] else 'false'
    service_provider_user = mongo.db.users.find_one({"user_id": service_provider})
    service_requester_user = mongo.db.users.find_one({"user_id": service_requester})
    service_approved = 'none'
    for notification in user['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['message_id']:
            mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['message_id']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'read'} })
            status = notification['status']
            try:
                service_approved = {}
                service_approved['completion_date'] = notification['completion_date']
                completion_date = datetime.datetime.strptime(service_approved['completion_date'], '%Y-%m-%d').date()
                days_to_go = (completion_date - datetime.date.today()).days
                service_approved['days_to_go'] = days_to_go if int(days_to_go) > 0 else 'Deadline Reached'
            except:
                service_approved = 'none'
            break
    return render_template('profile/service_request_chat.html', messages=messages, user=user['user_id'], service_provider=service_provider_user, service_requester=service_requester_user, service_approved=service_approved, status=status)

@profile_blueprint.route('/send_message', methods=['POST'])
def send_message():
    messages = mongo.db.messages.find_one({"message_id": request.form['message_id']})
    user = mongo.db.users.find_one({"email": session['user_email']})
    send_to = [messages['users']['service_provider'], messages['users']['service_requester']]
    send_to.remove(user['user_id'])
    new_message = {
        'message': request.form['message'],
        'date_time': str(datetime.date.today()),
        'read_status': 'unread',
        'sent_by': user['user_id']
    }
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$push": {'messages': new_message}})
    mongo.db.users.find_one_and_update({"user_id": send_to[0]}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    for notification in user['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['message_id']:
            status = notification['status']
            mongo.db.users.find_one_and_update({"user_id": send_to[0], 'profile.notifications.notifications_list.messages_id': request.form['message_id']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    #send_to_email = mongo.db.users.find_one({"user_id": send_to[0]})
    #subject = "New Message"
    #html = render_template('account/new_message_email.html')
    #send_email(send_to_email['email'], subject, html)
    return render_template('profile/service_request_chat.html', messages=messages, user=user['user_id'], service_approved='none', status=status)


################# SERVICE HANDLING ###################

@profile_blueprint.route('/add_service', methods=['POST'])
def add_service():
    service = {}
    service['title'] = request.form['service_title']
    service['cost'] = request.form['service_cost'] if len(request.form['service_cost']) > 0 else 0
    service['description'] = request.form['service_description']
    mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$push": {'profile.services': service}})
    return render_template('profile/profile_add_service.html', service=service)

@profile_blueprint.route('/approve_service_request', methods=['POST'])
def approve_service_request():
    date_conversion = datetime.datetime.strptime(request.form['date'].replace('/', ''), "%d%m%Y").date()
    message = mongo.db.messages.find_one({"message_id": request.form['service_request']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    for notification in service_requester['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['service_request']:
            service_requester_message = dict(new_message)
            service_requester_message['private_to'] = service_requester['user_id']
            service_provider_message = dict(new_message)
            service_provider_message['private_to'] = service_provider['user_id']
            mongo.db.users.find_one_and_update({"user_id": service_requester['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
            if notification['status']['provider_acceptance'] == 'accepted':
                date_exists = notification['completion_date']
                service_requester_message['message'] = service_provider['profile']['username'] + " would like to change the deadline for your service request. Do you accept the following date change - New Date: " + str(date_conversion)
                service_requester_message['type'] = 'prompt'
                service_requester_message['subtype'] = 'deadline_extension_request'
                service_requester_message['prompt_options'] = ['no', 'yes']
                service_provider_message['message'] = "You requested a deadline change to " + str(date_conversion) + " for this service request."
                form_response_message = "Your deadline change request has been sent and will be updated if " + service_requester['profile']['username'] + " accepts the new date."
            else:
                service_requester_message['type'] = 'text'
                service_requester_message['message'] = "Great news, " + service_provider['profile']['username'] + " has approved your service request!"
                service_provider_message['message'] = "You approved this service request and you will be informed when their payment transfer has been finialized."
                form_response_message = "You have successfully approved this service request!"
                for user in [service_provider, service_requester]:
                    mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'accepted', "profile.notifications.notifications_list.$.status.provider_acceptance": 'accepted', "profile.notifications.notifications_list.$.completion_date": str(date_conversion)} })
            break
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    return render_template('profile/_service_request_form_success.html', message=form_response_message)

@profile_blueprint.route('/cancel_service_request', methods=['POST'])
def cancel_service_request():
    message = mongo.db.messages.find_one({"message_id": request.form['service_request']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_requester_message['message'] = "This service request has been cancelled."
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    service_provider_message['message'] = "This service request has been cancelled."
    form_response_message = "This service request has been cancelled. You can view it in your archive."
    for user in [service_provider, service_requester]:
        mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'cancelled', "profile.notifications.notifications_list.$.status.provider_completion": 'cancelled'} })
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    for notification in service_provider['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['service_request']:
            if notification['status']['requester_charge'] == 'true':
                days_to_go = (completion_date - datetime.date.today()).days
                if int(days_to_go) <= 0:
                    stripe.api_key = os.environ['SECRET_STRIPE_KEY']
                    refund = stripe.Refund.create(charge=messages['stripe_charge_id'])
    return render_template('profile/_service_request_form_success.html', message=form_response_message)

@profile_blueprint.route('/complete_service_request', methods=['POST'])
def complete_service_request():
    message = mongo.db.messages.find_one({"message_id": request.form['service_request']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_requester_message['message'] = service_provider['profile']['username'] + " has marked your service request as complete! Do you agree?"
    service_requester_message['type'] = 'prompt'
    service_requester_message['subtype'] = 'confirm_service_request_completion'
    service_requester_message['prompt_options'] = ['no', 'yes']
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    service_provider_message['message'] = "You marked this service request as complete!"
    form_response_message = "You have completed this service request! Your payement will be processed either when " + service_requester['profile']['username'] + " confirms or when the deadline date is reached."
    for user in [service_provider, service_requester]:
        mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'complete', "profile.notifications.notifications_list.$.status.provider_completion": 'complete'} })
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    return render_template('profile/_service_request_form_success.html', message=form_response_message)

@profile_blueprint.route('/complete_transaction', methods=['POST'])
def complete_transaction():
    message = mongo.db.messages.find_one({"message_id": request.form['service_request']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_requester_message['message'] = "This service request transaction is officially complete! Feel free to leave a review."
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    service_provider_message['message'] = "This service request transaction is officially complete! You can transfer your earnings to your bank account from the Earnings page."
    for user in [service_provider, service_requester]:
        mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'completion_confirmed', "profile.notifications.notifications_list.$.status.completion_confirmed": 'true'} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$pull": {'messages': { 'type': 'prompt'}}})
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    return redirect(url_for('profile.notifications_page'))

@profile_blueprint.route('/create_service_request', methods=['POST'])
def create_service_request():
    service_provider = mongo.db.users.find_one({"user_id": request.form['service'].rsplit('--', 1)[0]})
    service_requester = mongo.db.users.find_one({"email": session['user_email']})
    service_request = {
        'service_provider': service_provider['user_id'],
        'service_requester': service_requester['user_id'],
        'service': request.form['service'].rsplit('--', 1)[1],
        'status': {'current_status': "acceptance_pending", 
           'provider_acceptance': "pending", 
           'requester_charge': "false", 
           'provider_completion': "pending",
           'completion_confirmed': "true/false",
           'payout_processed': "false", 
           'requester_reviewed': "false"},
        'date_time_request_sent': str(datetime.date.today()),
        'date_time_last_message': "",
        'messages_id': "",
        'read_status': "unread"
    }
    message_class = Message()
    service = [service for service in service_provider['profile']['services'] if service['title'] == request.form['service'].rsplit('--', 1)[1]][0]
    message_insert = {'service_provider': service_provider['user_id'], 'service_requester': service_requester['user_id'], 'service': service}
    message = message_class.template(message_insert)
    message_id = mongo.db.messages.insert(message)
    mongo.db.messages.find_one_and_update({'_id': message_id}, {"$set": {"message_id": str(message_id)}})
    service_request['messages_id'] = str(message_id)
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_requester_message['message'] = "You sent a service request!"
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    service_provider_message['message'] = service_requester['profile']['username'] + " sent you a service request!"
    service_provider_message['type'] = 'text'
    mongo.db.messages.find_one_and_update({"message_id": str(message_id)}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": str(message_id)}, {"$push": {'messages': service_provider_message}})
    if len(request.form['message'] ) > 0:
        new_message = {
            'type': 'text',
            'message': request.form['message'],
            'date_time': str(datetime.date.today()),
            'read_status': "unread",
            'sent_by': service_requester['user_id']
        }
        mongo.db.messages.find_one_and_update({'_id': message_id}, {"$push": {"messages": new_message}})
        service_request['date_time_last_message'] = str(datetime.date.today())
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id']}, {"$push": {'profile.notifications.notifications_list': service_request}})
    mongo.db.users.find_one_and_update(
        {"user_id": service_provider['user_id']}, 
        {
            "$push": {'profile.notifications.notifications_list': service_request},
            "$set": {'profile.notifications.new_notifications': 'yes'}
        }
    )
    return redirect(url_for('profile.notifications_page'))

@profile_blueprint.route('/date_change_response', methods=['POST'])
def date_change_response():
    message = mongo.db.messages.find_one({"message_id": request.form['service_request']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    if request.form['response'] == 'reject':
        service_requester_message['message'] = "You declined " + service_provider['profile']['username'] + "'s deadline change request. You can cancel this service request in the Update tab."
        service_provider_message['message'] = "Unfortunately, " + service_requester['profile']['username'] + " has declined your deadline change request. You can cancel this service request in the Update tab."
    else:
        service_requester_message['message'] = "You accepted " + service_provider['profile']['username'] + "'s deadline change."
        service_provider_message['message'] = "Good news! " + service_requester['profile']['username'] + " has accepted your deadline change."
        for user in [service_provider, service_requester]:
            mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'accepted', "profile.notifications.notifications_list.$.status.provider_acceptance": 'accepted', "profile.notifications.notifications_list.$.completion_date": request.form['date']} })
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$pull": {'messages': { 'type': 'prompt'}}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    return redirect(url_for('profile.notifications_page'))

@profile_blueprint.route('/reject_service_request', methods=['POST'])
def reject_service_request():
    message = mongo.db.messages.find_one({"message_id": request.form['service_request']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_requester_message['message'] = "Unfortunately, " + service_provider['profile']['username'] + " has declined your service request at this time."
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    service_provider_message['message'] = "You declined this service request."
    form_response_message = "You have rejected this service request and can view it in your archive."
    for user in [service_provider, service_requester]:
        mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'rejected', "profile.notifications.notifications_list.$.status.provider_acceptance": 'rejected'} })
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['service_request']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['service_request']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    return render_template('profile/_service_request_form_success.html', message=form_response_message)

@profile_blueprint.route('/review_service_request', methods=['POST'])
def review_service_request():
    message = mongo.db.messages.find_one({"message_id": request.form['message_id']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_requester_message['message'] = "You successfully submitted a review."
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    review_rating = " | Rating: " + str(request.form['rating']) + "/5 stars" if len(request.form['rating']) > 0 else ""
    review_message = " | Message: " + request.form['message'] if len(request.form['message']) > 0 else ""
    service_provider_message['message'] = service_requester['profile']['username'] + " submitted a review of your service." + review_rating + review_message
    form_response_message = "You successfully submitted a review."
    for user in [service_provider, service_requester]:
        mongo.db.users.find_one_and_update({"user_id": user['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['message_id']}, {"$set": {"profile.notifications.notifications_list.$.status.current_status": 'reviewed', "profile.notifications.notifications_list.$.status.requester_reviewed": 'true'} })
    review = {'user': service_requester['user_id'], 'service': request.form['message_id'], 'rating': request.form['rating'], 'message': request.form['message']}
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['message_id']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'}, "$push": {"profile.reviews": review} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$set": {'review': review}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_provider['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    return render_template('profile/_service_request_form_success.html', message=form_response_message)
    
@profile_blueprint.route('/edit_service', methods=['POST'])
def edit_service():
    old_service = {}
    old_service['title'] = request.form['old_service_title']
    old_service['cost'] = request.form['old_service_cost'].strip('$')
    old_service['description'] = request.form['old_service_description']
    new_service = {}
    new_service['title'] = request.form['new_service_title']
    new_service['cost'] = request.form['new_service_cost'].strip('$')
    new_service['description'] = request.form['new_service_description']
    mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$pull": {'profile.services': old_service}})
    mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$push": {'profile.services': new_service}})
    return 'true'
    
@profile_blueprint.route('/edit_service_request', methods=['POST'])
def edit_service_request():
    message = mongo.db.messages.find_one({"message_id": request.form['message_id']})
    service_provider = mongo.db.users.find_one({"user_id": message['users']['service_provider']})
    service_requester = mongo.db.users.find_one({"user_id": message['users']['service_requester']})
    new_message = {
        'type': 'text',
        'message': '',
        'date_time': str(datetime.date.today()),
        'sent_by': 'status update'
    }
    service_requester_message = dict(new_message)
    service_requester_message['private_to'] = service_requester['user_id']
    service_requester_message['message'] = service_provider['profile']['username'] + " has updated the details of your service request."
    service_provider_message = dict(new_message)
    service_provider_message['private_to'] = service_provider['user_id']
    service_provider_message['message'] = "You updated the details of this service request."
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id'], 'profile.notifications.notifications_list.messages_id': request.form['message_id']}, {"$set": {"profile.notifications.notifications_list.$.read_status": 'unread'} })
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$push": {'messages': service_requester_message}})
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$push": {'messages': service_provider_message}})
    mongo.db.users.find_one_and_update({"user_id": service_requester['user_id']}, {"$set": {'profile.notifications.new_notifications': 'yes'}})
    old_service = {}
    old_service['title'] = request.form['old_service_title']
    old_service['cost'] = request.form['old_service_cost'].strip('$')
    old_service['description'] = request.form['old_service_description']
    old_service['date_changed'] = str(datetime.date.today())
    new_service = {}
    new_service['title'] = request.form['new_service_title']
    new_service['cost'] = request.form['new_service_cost'].strip('$')
    new_service['description'] = request.form['new_service_description']
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$set": {'service': new_service}, "$push": {'service_archive': old_service}}) 
    return 'true'
    
@profile_blueprint.route('/remove_service', methods=['POST'])
def remove_service():
    service = {}
    service['title'] = request.form['service_title']
    service['cost'] = request.form['service_cost'].strip('$')
    service['description'] = request.form['service_description']
    mongo.db.users.find_one_and_update({"email": session['user_email']}, {"$pull": {'profile.services': service}})
    return 'true'
    
@profile_blueprint.route('/add_service_suggestion', methods=['POST'])
def add_service_suggestion():
    career = mongo.db.careers.find_one({"career_id": request.form['career']})
    if request.form['service_title'] in [service['title'] for service in career['services']['suggestions']]:
        mongo.db.careers.find_one_and_update({"career_id": request.form['career']}, {"$pull": {'services.suggestions.title': request.form['service_title']}})
    service = {}
    service['title'] = request.form['service_title']
    service['expert_description'] = request.form['service_expert_description']
    service['user_description'] = request.form['service_user_description']
    mongo.db.careers.find_one_and_update({"career_id": request.form['career']}, {"$push": {'services.suggestions': service}})
    return render_template('profile/profile_add_service.html', service=service)
    
@profile_blueprint.route('/service_request_info', methods=['POST'])
def service_request_info():
    user = mongo.db.users.find_one({"email": session['user_email']})
    return render_template('profile/service_request_info.html', user=user, service=mongo.db.messages.find_one({"message_id": request.form['message_id']}))
    
@profile_blueprint.route('/service_request_status', methods=['POST'])
def service_request_status():
    user = mongo.db.users.find_one({"email": session['user_email']})
    message = mongo.db.messages.find_one({"message_id": request.form['message_id']})
    for notification in user['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['message_id']:
            status = notification['status']
            service_provider = notification['service_provider']
            break
    return render_template('profile/service_request_status.html', message_id=request.form['message_id'], user=user['user_id'], message=message, service_provider=mongo.db.users.find_one({"user_id": service_provider}), status=status)
    
@profile_blueprint.route('/service_request_update', methods=['POST'])
def service_request_update():
    user = mongo.db.users.find_one({"email": session['user_email']})
    message = mongo.db.messages.find_one({"message_id": request.form['message_id']})
    for notification in user['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['message_id']:
            status = notification['status']
            break
    return render_template('profile/service_request_update.html', message_id=request.form['message_id'], user=user, message=message, status=status)
    
@profile_blueprint.route('/cancel_service_form')
def cancel_service_form():
    return render_template('profile/service_request_update_forms/cancel_service_form.html')
    
@profile_blueprint.route('/accept_service_form')
def accept_service_form():
    return render_template('profile/service_request_update_forms/accept_service_form.html')
    
@profile_blueprint.route('/review_service_form')
def review_service_form():
    return render_template('profile/service_request_update_forms/review_service_form.html')
    
@profile_blueprint.route('/pay_for_service_form', methods=['POST'])
def pay_for_service_form():
    return render_template('profile/service_request_update_forms/pay_for_service_form.html', messages=mongo.db.messages.find_one({"message_id": request.form['message_id']}))
    
@profile_blueprint.route('/mark_service_as_complete_form')
def mark_service_as_complete_form():
    return render_template('profile/service_request_update_forms/mark_service_as_complete_form.html')
    
@profile_blueprint.route('/service_deadline_form', methods=['POST'])
def service_deadline_form():
    user = mongo.db.users.find_one({"email": session['user_email']})
    for notification in user['profile']['notifications']['notifications_list']:
        if notification['messages_id'] == request.form['message_id']:
            status = notification['status']
            break
    return render_template('profile/service_request_update_forms/service_deadline_form.html', status=status)
    
@profile_blueprint.route('/update_service_request_cost', methods=['POST'])
def update_service_request_cost():
    new_service_cost = request.form['new_service_cost'].strip('$')
    mongo.db.messages.find_one_and_update({"message_id": request.form['message_id']}, {"$set": {'service.cost_update': new_service_cost}})
    return 'true'
    
@profile_blueprint.route('/remove_service_suggestion', methods=['POST'])
def remove_service_suggestion():
    mongo.db.careers.find_one_and_update({"career_id": request.form['career']}, {"$pull": {'services.suggestions':{'title': request.form['service_title']}}})
    return 'true'