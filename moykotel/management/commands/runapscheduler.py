import logging
from django.contrib.auth.models import User
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import datetime

from moykotel.models import Post, Subscriber
import moykotel.settings


logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=30)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(posts.filter(post_date__gte=last_week).values_list('post_category', flat=True))
    users = set(Subscriber.objects.all().values_list('user', flat=True))

    for subscriber in users:
        categories_subscriber = set(Subscriber.objects.filter(user=subscriber).values_list('category_id', flat=True))
        categories_newsletter = categories & categories_subscriber
        posts_list = posts.filter(
            post_category__in=categories_newsletter
        )

        html_content = render_to_string(
            'mail/categories_weekly_email.html',
            {
                'link': settings.SITE_URL,
                'posts': posts_list,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=list(User.objects.filter(pk=subscriber).values_list('email', flat=True)),
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon-fri", hour="23", minute="47"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")