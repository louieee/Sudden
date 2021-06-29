from abc import ABC, abstractmethod

from rest_framework import status

from utilities.api_response import APIFailure


class APIRequiredMixin(ABC):
    required_fields = ()

    def check_required(self, request):
        fields_ = [request.data.get(x, None) for x in self.required_fields if request.data.get(x, None) is None]
        return fields_.__len__() == 0

    def error_response(self):
        return APIFailure(f"The required fields are {', '.join(self.required_fields)}",
                          status=status.HTTP_400_BAD_REQUEST)