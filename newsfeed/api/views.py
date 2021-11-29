from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from apiconsumer.api.serializers import TopHeadlineModelSerializer
from newsfeed.models import NewsFeedModel


class NewsFeedView(ListAPIView):
    serializer_class = TopHeadlineModelSerializer

    authentication_class = [TokenAuthentication]
    permission_class = [IsAuthenticated]

    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        feed = NewsFeedModel.objects.get(user=self.request.user)
        return feed.topHeadlines.all()
