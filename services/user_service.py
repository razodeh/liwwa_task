from sqlalchemy.exc import IntegrityError

from exceptions import TinyHRError
from services.base import CRUDServiceBase
from models import User, DB, CandidateProfile
from uploaders import FileSystemStorage


class UserService(CRUDServiceBase):
    def create(self, user_details, profile_details=None, **kwargs):
        try:
            # Put User Details
            user = User(**user_details, **kwargs)
            DB.session.add(user)
            DB.session.commit()
            # Hash User's Password
            user.hashify_password(user.password)
            if profile_details:
                profile = CandidateProfile(**profile_details, user_id=user.id)
                DB.session.add(profile)
            DB.session.add(user)
            DB.session.commit()
        except IntegrityError:
            raise TinyHRError(
                f"User with email '{user_details['email']}' already exist."
            )
        return user

    def list(self, page=1, per_page=10, **kwargs):
        users_list = User.query.filter_by(is_admin=False).order_by(
            User.date_joined.desc()
        ).paginate(
            page, per_page, error_out=False
        ).items
        return [self.serialize_listing(user) for user in users_list]

    def retrieve(self, pk, **kwargs):
        return User.query.filter_by(id=pk).first_or_404()

    def destroy(self, pk, **kwargs):
        pass

    def update(self, pk, **kwargs):
        pass

    def serialize_listing(self, instance):
        serialized = {
            "full_name": f"{instance.first_name} {instance.last_name}",
            "years_of_experience": instance.profile and instance.profile.years_of_experience,
            "department": instance.profile and instance.profile.department.name.upper(),
            "date_of_birth": instance.profile and instance.profile.date_of_birth,
        }
        return serialized

    def authenticate_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        # Checking if user credentials are correct
        if user and user.authenticate(password=password):
            return user
        # Throw and Error on failure.
        raise TinyHRError("Invalid Credentials", 401)

    def upload_resume(self, user, resume_file):
        user_profile = user.profile
        file_path = FileSystemStorage().upload_file(resume_file)
        user_profile.resume_url = file_path
        DB.session.add(user_profile)
        DB.session.commit()

    def get_user_resume(self, pk):
        user = self.retrieve(pk)
        resume_path = user.profile.resume_url
        resume_file = FileSystemStorage().retrieve_file(resume_path)
        return resume_file
