from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from api.serializers import BookReviewSerializer


from books.models import Book, BookReview

# Create your views here.

# class BookReviewDetailApiView(APIView):
#     def get(self, request, pk):
#         book_review = BookReview.objects.get(pk=pk)

#         json_response = {
#             'pk': book_review.pk,
#             'stars_given': book_review.stars_given,
#             'comment': book_review.comment,
#             'user_id': {
#                 'pk': book_review.user_id.pk,
#                 'username': book_review.user_id.username,
#                 'first_name': book_review.user_id.first_name,
#                 'last_name': book_review.user_id.last_name,
#                 'email': book_review.user_id.email,
#             },
#             'book_id': {
#                 'id': book_review.book_id.pk,
#                 'title': book_review.book_id.title,
#                 'description': book_review.book_id.description,
#             },
#         }

#         return JsonResponse(json_response)

# View sets

class BookReviewViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated, ]
    serializer_class = BookReviewSerializer  
    queryset = BookReview.objects.all().order_by('-created_at')



# Generics views

# # class BookReviewDetailApiView(APIView):
# #     permission_classes = [IsAuthenticated]
 
# #     def get(self, request, pk):
# #         book_review = BookReview.objects.get(pk=pk)
# #         serializer = BookReviewSerializer(book_review)
 
# #         return Response(data=serializer.data)
 
# #     def delete(self, request, pk):
# #         book_review = BookReview.objects.get(pk=pk)
# #         book_review.delete()
 
# #         return Response(status=status.HTTP_204_NO_CONTENT)

# #     def patch(self, request, pk):
# #         book_review = BookReview.objects.get(pk=pk)
# #         serializer = BookReviewSerializer(instance=book_review, data=request.data, partial=True)
       
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(data=serializer.data, status=status.HTTP_200_OK)

# #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# #     def put(self, request, pk):
# #         book_review = BookReview.objects.get(pk=pk)
# #         serializer = BookReviewSerializer(instance=book_review, data=request.data)
        
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(data=serializer.data, status=status.HTTP_200_OK)
# #
# #        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

# class BookReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated, ]
#     serializer_class = BookReviewSerializer
#     queryset = BookReview.objects.all()


# # class BookReviewApiView(APIView):
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = BookReviewSerializer
    
# #     def get(self, request):
# #         book_reviews = BookReview.objects.all().order_by('-created_at')

# #         paginator = PageNumberPagination()
# #         page_obj = paginator.paginate_queryset(book_reviews, request)

# #         serializer = self.serializer_class(page_obj, many=True)

# #         return paginator.get_paginated_response(serializer.data)

# #     def post(self, request, *args, **kwargs):
# #         serializer = self.serializer_class(data=request.data)

# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
# #         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class BookReviewApiView(generics.ListCreateAPIView):
#     permission_classes=[IsAuthenticated, ]
#     serializer_class = BookReviewSerializer  
#     queryset = BookReview.objects.all().order_by('-created_at')
