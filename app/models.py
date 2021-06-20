from app import mongo
import datetime
    
    
# ++++++++++++++++++++++++++++
# 	ADMIN COLLECTION
# ++++++++++++++++++++++++++++

class Admin:
    def template(self, username, name, hashpass):
        return { 
            'admin_id': "",
            'username': username,
            'name': name,
            'password' : hashpass
        }
    
    def admin(self):
        return {
            "_id": {
                "$oid": "5b6a2672fa1051393fc54560"
            },
            "name": "Lamar",
            "admin_id": "",
            "username": "admin_lamar",
            "password": "sha256$eY39fPlN$030c789414b8a88f30891f657a96fc9bb46050348f5c7c61991e976414db8efa",
            "user_id": "5b6a2672fa1051393fc54560",
            "colls": [
                {
                    "title": "",
                    "url": "",
                    "image": "",
                    "text": "",
                    "tags": [],
                    "careers": [],
                    "action": ""
                }
            ],
            "services": {
               "suggestions_basic": [{"title": "", "expert_description": "", "user_description": ""}],
               "suggestions_bank": [{"title": "", "expert_description": "", "user_description": ""}]
            },
            "invitations": [
                {
                    "code": "", 
                    "requester": "", 
                    "expert_social": "", 
                    "expert_username": "", 
                    "service": {'title': "", 'cost': "", 'message': ""}, 
                    "date_time_request_sent": "", 
                    "status": "pending/archived"
                }
            ]
        }
    

# ++++++++++++++++++++++++++++
# 	MESSAGE COLLECTION
# ++++++++++++++++++++++++++++

class Message:
    def template(self, message):
        return {
            'message_id': "",
            'users': {
                'service_provider': message['service_provider'],
                'service_requester': message['service_requester']
            },
            'service': message['service'], #{'title': "", 'cost': "", 'description': ""}
            #'service_archive': [{date_changed: "", 'title': "", 'cost': "", 'description': ""}]
            'stripe_charge_id': "",
            'review': "",
            'messages': [
                #{
                #    'message': "",
                #    'date_time': "",
                #    'type': "", #['text', 'prompt']
                #    'subtype': "", #[approve_decline_service_request, 'deadline_extension_request', 'service_charge', 
                #                   'confirm_service_request_completion']
                #    'read_status': "",
                #    'sent_by': "",
                #    'private_to': "",
                #}
            ]
        }
    

# ++++++++++++++++++++++++++++
# 	CAREER COLLECTION
# ++++++++++++++++++++++++++++

#class Career:
#    def template(self):
#        return { 
#            "career_id": "",
#            "title": "",
#            "alternative_titles": [],
#            "description": "",
#            "image": "",
#            "videos": [],
#            "tags": []
#            "users": [],
#            "services": {"suggestions": []}
#        }

# ++++++++++++++++++++++++++++
# 	USERS COLLECTION
# ++++++++++++++++++++++++++++

class User:
    def template(self, email, username, hashpass):
        return {
            'user_id': "",
            'email': email,
            'password': hashpass,
            'account_creation_date': str(datetime.date.today()),
            "bookmarks": {'careers': [], 'collections': [], 'profiles': []},
            'profile': {
                'username': username,
                'name': "",
                'visible': "false",
                'careers': [],
                'profile_image': {'type': "", 'src': ""},
                'header_image': {'type': "", 'src': ""},
                'description': "",
                'social_media': {"linkedin": "", "twitter": "", "instagram": "", "facebook": "", "pinterest": "", "youtube": ""},
                'links': [],
                'earnings': {'potential_earnings': "", 'pending_earnings': "", 'earnings_to_date': "" },
                'reviews': [],
                'notifications': {'new_notifications': "no", 'notifications_list': []},
                'services': []
            },
            "stripe": {
                "stripe_customer_id": "",
                "stripe_connect" : { "code": "", "account_id": "" }
            }
        }

#class User:
#    def template(self, email, name, hashpass):
#        return { 
#            'user_id': "",
#            'email': email,
#            'password': hashpass,
#            'account_creation_date': str(datetime.date.today()),
#            'account_verified': 0,
#            'account_verified_on': "",
#            'stripe': {
#                'stripe_customer_id': "",
#                'stripe_connect' : { "code": null, "account_id": "" }
#            }
#            "bookmarks": { 'careers': [], 'collections': [], 'profiles': [] },
#            'profile': {
#               'username': "",
#               'name': name,
#               'visible': "false",
#               'profile_image': {'type': "", 'src': ""},
#               'header_image': {'type': "", 'src': ""},
#               'description': "",
#               'social_media': {"linkedin": "", "twitter": "", "instagram": "", "facebook": "", "pinterest": "", "youtube": ""},
#               'links': [],
#               'earnings': { 'potential_earnings': "", 'pending_earnings': "", 'earnings_to_date': "" },
#               'reviews': [{'user': "", 'service': "", 'rating': "", 'message': ""}],
#               'reviews': [{'user': "", 'service': "", 'rating': "", 'message': ""}],
#               'invitations': [],
#               'notifications': {
#                   'new_notifications': "", #['yes', 'no']
#                   'notifications_list': [
#                       {
#                           'requested_by': "",
#                           'service_provider': "",
#                           'messages_id': "",
#                           'read_status': "", #['read', 'unread']
#                           'service': "",
#                           'status': {'current_status': "", #[acceptance_pending, accepted, rejected, charge_processed, complete, 
#                                                              completion_confirmed, cancelled, payout_processed, reviewed]
#                                      'provider_acceptance': "pending/accepted/rejected", 
#                                      'requester_charge': "true/false", 
#                                      'provider_completion': "pending/complete/cancelled", 
#                                      'completion_confirmed': "true/false", 
#                                      'payout_processed': "true/false", 
#                                      'requester_reviewed': "true/false"}
#                           'date_time_request_sent': "",
#                           'date_time_last_message': "",
#                           'completion_date': ""
#                       }
#                   ]
#               },
#               'services': [
#                   { 'title': "", 'cost': "", 'description': "" }
#               ]
#           }
#        }