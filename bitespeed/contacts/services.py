from .models import Contact
from django.db import models

def format_contact_response(primary_contact, secondary_contacts):
    emails = [primary_contact.email] + [contact.email for contact in secondary_contacts if contact.email]
    phone_numbers = [primary_contact.phone_number] + [contact.phone_number for contact in secondary_contacts if contact.phone_number]
    secondary_contact_ids = [contact.id for contact in secondary_contacts]

    return {
        "primaryContatctId": primary_contact.id,
        "emails": emails,
        "phoneNumbers": phone_numbers,
        "secondaryContactIds": secondary_contact_ids
    }

class Service():

    def find_or_create_contact(email=None, phone_number=None):
        existing_contacts = Contact.objects.filter(
        models.Q(email=email) | models.Q(phone_number=phone_number)
        ).order_by('created_at')
        if not existing_contacts.exists():
        # Create new primary contact
            primary_contact = Contact.objects.create(email=email, phone_number=phone_number, link_precedence='primary')
            return format_contact_response(primary_contact, [])

        primary_contact = existing_contacts.filter(link_precedence='primary').first()
        if not primary_contact:
            # If there is no primary contact, the first contact in the list is the primary one
            primary_contact = existing_contacts.first()
            primary_contact.link_precedence = 'primary'
            primary_contact.save()
        secondary_contacts = existing_contacts.exclude(id=primary_contact.id)

        # Handle the creation of new secondary contacts if needed
        if email and not existing_contacts.filter(email=email).exists():
            new_secondary_contact = Contact.objects.create(
                email=email,
                phone_number=primary_contact.phone_number,
                linked_id=primary_contact,
                link_precedence='secondary'
            )
            secondary_contacts = secondary_contacts | Contact.objects.filter(pk=new_secondary_contact.pk)

        if phone_number and not existing_contacts.filter(phone_number=phone_number).exists():
            new_secondary_contact = Contact.objects.create(
                email=primary_contact.email,
                phone_number=phone_number,
                linked_id=primary_contact,
                link_precedence='secondary'
            )
            secondary_contacts = secondary_contacts | Contact.objects.filter(pk=new_secondary_contact.pk)

        # Handle merging of primary contacts
        if email and phone_number:
            linked_primary_contacts = Contact.objects.filter(
                models.Q(email=email) | models.Q(phone_number=phone_number),
                link_precedence='primary'
            ).order_by('created_at')
            if linked_primary_contacts.count() > 1:
                oldest_primary = linked_primary_contacts.first()
                for primary in linked_primary_contacts.exclude(id=oldest_primary.id):
                    primary.linked_id = oldest_primary
                    primary.link_precedence = 'secondary'
                    primary.save()
                    secondary_contacts = secondary_contacts | Contact.objects.filter(pk=primary.pk)

        return format_contact_response(primary_contact, secondary_contacts)