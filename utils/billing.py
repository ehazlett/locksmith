#!/usr/bin/env python
# Copyright 2012 Evan Hazlett
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import stripe
from django.conf import settings
from django.utils.translation import ugettext as _

# set stripe api key
stripe.api_key = getattr(settings, 'STRIPE_API_KEY')

def create_customer(token=None, plan=None, email=None):
    customer = stripe.Customer.create(
        card=token,
        plan=plan,
        email=email
    )
    return customer

def charge(amount=None, currency='usd', card_number=None,
    card_exp_month=None, card_exp_year=None, card_cvc=None, card_name=None,
    description='Locksmith Payment'):
    """
    Charges specified credit card for account
    
    :param amount: Amount in dollars
    :param currency: Currency (default: usd)
    :param card_number: Credit card number
    :param card_exp_month: Credit card expiration month (two digit integer)
    :param card_exp_year: Credit card expiration year (two or four digit integer)
    :param card_cvc: Credit card CVC
    :param card_name: Credit cardholder name
    :param description: Charge description (default: Locksmith Payment)

    """
    # convert amount to cents
    amount = int(amount * 100)
    card_info = {
        'number': card_number.replace('-', ''),
        'exp_month': card_exp_month,
        'exp_year': card_exp_year,
        'cvc': card_cvc,
        'name': card_name,
    }
    data = {}
    try:
        charge = stripe.Charge.create(amount=amount, currency=currency, card=card_info,
            description=description)
        if charge.paid:
            data['status'] = True
            data['message'] = _('Thanks!')
        else:
            data['status'] = False
            data['message'] = charge.failure_message
        data['created'] = charge.created
    except Exception, e:
        data['status'] = False
        data['message'] = e
    return data
