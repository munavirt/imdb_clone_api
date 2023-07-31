from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    # writing this code for permission if the staff user can only read the data they cant do otherthing with that data(like put,delete,post)
    # but the user is admin they can do anythin
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        
    
    

#using of this class [ if the logged user and review user are same they can edit that review and they can edit but thats not review user they can only read that data]
class IsReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: #if they accessing send(get) request
            return True
        else:                                           #if they are trying post request or other request
            return obj.review_user == request.user or request.user.is_staff