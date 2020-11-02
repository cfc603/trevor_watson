from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtailcodeblock.blocks import CodeBlock

from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, MultiFieldPanel
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class Index(Page):

    sub_title = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("sub_title"),
        FieldPanel("description", classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        """
            Adding custom stuff to our context.
            https://learnwagtail.com/tutorials/how-to-paginate-your-wagtail-pages/
        """
        context = super().get_context(request, *args, **kwargs)

        # Get all posts
        all_posts = self.get_posts(request.GET.get("tag"))

        # Paginate all posts by 5 per page
        paginator = Paginator(all_posts, 5)

        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts

        context["tags"] = TaggitTag.objects.filter(post__isnull=False).distinct()
        return context

    def get_posts(self, tag=None):
        posts = Post.objects.live().public()
        if tag:
            posts = posts.filter(tags__name=tag)
        posts = posts.order_by("-first_published_at")
        return posts


class Post(Page):

    date = models.DateField("Post Date")
    intro = models.CharField(max_length=255)
    body = StreamField([
        ("heading", blocks.CharBlock(classname="full title")),
        ("paragraph", blocks.RichTextBlock(
            features=[
                "h1", "h2", "h3", "h4", "h5", "h6", "bold", "italic", "ol",
                "ul", "hr", "link", "documen", "image", "embed", "code",
                "blockquote",
            ])
        ),
        ("image", ImageChooserBlock(classname="img-fluid")),
        ("code", CodeBlock()),
    ])
    tags = ClusterTaggableManager(through="Tag", blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel("date"), FieldPanel("tags")]),
        FieldPanel("intro", classname="full"),
        StreamFieldPanel("body"),
    ]

    def get_tags(self):
        return TaggitTag.objects.filter(post=self)


class Tag(TaggedItemBase):

    content_object = ParentalKey(
        "Post", related_name="tagged_items", on_delete=models.CASCADE
    )
