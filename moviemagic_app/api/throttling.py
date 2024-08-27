from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ReviewRateThrottle(UserRateThrottle):
    scope = 'review-create'
    
class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
    