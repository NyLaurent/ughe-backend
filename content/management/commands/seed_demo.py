from django.core.management.base import BaseCommand

from content.models import NavigationItem, SiteSettings, Slide, StatItem


class Command(BaseCommand):
    help = "Add starter UGHE homepage content when the corresponding tables are empty."

    def handle(self, *args, **options):
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name="University of Global Health Equity",
                logo_url="/assets/ughe-logo.png",
                facts_eyebrow="Our impact",
                facts_title="Facts & Stats",
            )

        if not NavigationItem.objects.exists():
            NavigationItem.objects.bulk_create(
                [
                    NavigationItem(label="Apply", url="#admissions", placement="header", sort_order=1),
                    NavigationItem(label="Get involved", url="#community", placement="header", sort_order=2),
                    NavigationItem(label="Meet the team", url="#team", placement="header", sort_order=3),
                    NavigationItem(label="More", url="#more", placement="header", sort_order=4),
                    NavigationItem(
                        label="Staff login",
                        url="/admin/",
                        placement="header",
                        kind="admin_login",
                        sort_order=5,
                    ),
                    NavigationItem(
                        label="Search",
                        url="https://ughe.org/?s=",
                        placement="header",
                        kind="search",
                        sort_order=6,
                    ),
                    NavigationItem(label="About Us", url="#about", show_dropdown=True, sort_order=1),
                    NavigationItem(label="Academics", url="#academics", show_dropdown=True, sort_order=2),
                    NavigationItem(label="Research", url="#research", sort_order=3),
                    NavigationItem(
                        label="Centres and Institutes",
                        url="#centres",
                        show_dropdown=True,
                        sort_order=4,
                    ),
                    NavigationItem(label="Admissions", url="#admissions", show_dropdown=True, sort_order=5),
                    NavigationItem(
                        label="News and Events",
                        url="#news",
                        show_dropdown=True,
                        sort_order=6,
                    ),
                ]
            )

        if not Slide.objects.exists():
            Slide.objects.bulk_create(
                [
                    Slide(
                        eyebrow="A new generation of leaders",
                        title="Building a more equitable future for global health",
                        description="Meet the people and ideas shaping a healthier, more equitable world from Butaro, Rwanda.",
                        button_label="Discover UGHE",
                        button_url="https://ughe.org/about-us/",
                        media_url="/assets/carousel-images/ughe1.jpg",
                        alt_text="UGHE students standing by the Butaro Campus sign",
                        sort_order=1,
                    ),
                    Slide(
                        eyebrow="Learn in a one-of-a-kind setting",
                        title="A campus designed for a healthier world",
                        description="Explore a learning community rooted in Rwanda and connected to the future of global health.",
                        button_label="Explore our campus",
                        button_url="https://ughe.org/",
                        media_url="/assets/carousel-images/ughe2.jpg",
                        alt_text="The University of Global Health Equity campus at dusk",
                        sort_order=2,
                    ),
                    Slide(
                        eyebrow="Learning that leads to impact",
                        title="Preparing leaders to transform health systems",
                        description="Our graduates take their knowledge and commitment into communities around the world.",
                        button_label="Meet our community",
                        button_url="https://ughe.org/",
                        media_url="/assets/carousel-images/ughe3.jpg",
                        alt_text="Graduates and faculty celebrating together",
                        sort_order=3,
                    ),
                    Slide(
                        eyebrow="Celebrating the next chapter",
                        title="Equipping changemakers to lead with purpose",
                        description="Join a community advancing health equity through education, research, and action.",
                        button_label="See our programs",
                        button_url="https://ughe.org/academics/",
                        media_url="/assets/carousel-images/ughe4.jpg",
                        alt_text="Graduates celebrating at a University of Global Health Equity ceremony",
                        sort_order=4,
                    ),
                    Slide(
                        eyebrow="A community of changemakers",
                        title="Meet the graduates moving global health forward",
                        description="Our students and alumni are strengthening health systems through leadership, service, and collaboration.",
                        button_label="Explore UGHE",
                        button_url="https://ughe.org/",
                        media_url="/assets/carousel-images/new/new1.jpg",
                        alt_text="UGHE graduates celebrating together",
                        sort_order=5,
                    ),
                    Slide(
                        eyebrow="Learning with global partners",
                        title="Connecting local leadership with global health expertise",
                        description="Partnerships help our community build practical skills and create lasting impact.",
                        button_label="Our partnerships",
                        button_url="https://ughe.org/",
                        media_url="/assets/carousel-images/new/new2.jpg",
                        alt_text="UGHE community members at a global health event",
                        sort_order=6,
                    ),
                    Slide(
                        eyebrow="Growing together",
                        title="Health equity starts with strong communities",
                        description="We work alongside communities to make quality health care more accessible to everyone.",
                        button_label="Learn about our work",
                        button_url="https://ughe.org/",
                        media_url="/assets/carousel-images/new/new3.jpg",
                        alt_text="Community members gathered at the UGHE Butaro Campus",
                        sort_order=7,
                    ),
                    Slide(
                        eyebrow="Rooted in Butaro, Rwanda",
                        title="A university with a global vision",
                        description="From Butaro to the world, UGHE prepares leaders to advance health equity.",
                        button_label="Visit UGHE",
                        button_url="https://ughe.org/",
                        media_url="/assets/carousel-images/new/new4.jpg",
                        alt_text="The UGHE Butaro Campus community",
                        sort_order=8,
                    ),
                ]
            )

        if not StatItem.objects.exists():
            StatItem.objects.bulk_create(
                [
                    StatItem(
                        value="128",
                        description="Community members trained through UGHE entrepreneurship initiatives",
                        sort_order=1,
                    ),
                    StatItem(
                        value="1,260",
                        description="Community members employed for campus projects",
                        sort_order=2,
                    ),
                    StatItem(
                        value="677",
                        description="Leaders across 61 countries trained in our Executive Education since 2016",
                        sort_order=3,
                    ),
                    StatItem(
                        value="4TH",
                        description="Among 129 universities in Sub-Saharan Africa (Times Higher Education Rankings 2024)",
                        sort_order=4,
                    ),
                ]
            )

        self.stdout.write(self.style.SUCCESS("Starter UGHE homepage content is ready."))
