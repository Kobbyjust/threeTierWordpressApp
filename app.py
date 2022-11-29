#!/usr/bin/env python3

import aws_cdk as cdk

from three_tier_wordpress_app.three_tier_wordpress_app_stack import ThreeTierWordpressAppStack


app = cdk.App()
ThreeTierWordpressAppStack(app, "three-tier-wordpress-app")

app.synth()
