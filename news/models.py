# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WpWpSeo404Links(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ctime = models.DateTimeField()
    link = models.CharField(unique=True, max_length=255, db_collation='utf8mb3_unicode_ci')
    referrer = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    ip = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci')
    country = models.CharField(max_length=100, db_collation='utf8mb3_unicode_ci')
    os = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci')
    browser = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci')

    class Meta:
        managed = False
        db_table = 'wp_WP_SEO_404_links'


class WpWpSeoCache(models.Model):
    id = models.PositiveIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    is_redirected = models.PositiveIntegerField()
    redirect_from = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    redirect_to = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    redirect_type = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_WP_SEO_Cache'


class WpWpSeoRedirection(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    enabled = models.IntegerField()
    redirect_from = models.CharField(unique=True, max_length=255, db_collation='utf8mb3_unicode_ci')
    redirect_from_type = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    redirect_from_folder_settings = models.IntegerField()
    redirect_from_subfolders = models.IntegerField()
    redirect_to = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    redirect_to_type = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    redirect_to_folder_settings = models.IntegerField()
    regex = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    redirect_type = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    url_type = models.IntegerField()
    postid = models.PositiveIntegerField(db_column='postID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_WP_SEO_Redirection'


class WpWpSeoRedirectionLog(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rid = models.PositiveIntegerField(db_column='rID', blank=True, null=True)  # Field name made lowercase.
    postid = models.PositiveIntegerField(db_column='postID', blank=True, null=True)  # Field name made lowercase.
    ctime = models.DateTimeField()
    rfrom = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    rto = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    rtype = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    rsrc = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci')
    referrer = models.CharField(max_length=255, db_collation='utf8mb3_unicode_ci')
    ip = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci')
    country = models.CharField(max_length=100, db_collation='utf8mb3_unicode_ci')
    os = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci')
    browser = models.CharField(max_length=20, db_collation='utf8mb3_unicode_ci')

    class Meta:
        managed = False
        db_table = 'wp_WP_SEO_Redirection_LOG'


class WpActionschedulerActions(models.Model):
    action_id = models.BigAutoField(primary_key=True)
    hook = models.CharField(max_length=191)
    status = models.CharField(max_length=20)
    scheduled_date_gmt = models.DateTimeField(blank=True, null=True)
    scheduled_date_local = models.DateTimeField(blank=True, null=True)
    args = models.CharField(max_length=191, blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)
    group_id = models.PositiveBigIntegerField()
    attempts = models.IntegerField()
    last_attempt_gmt = models.DateTimeField(blank=True, null=True)
    last_attempt_local = models.DateTimeField(blank=True, null=True)
    claim_id = models.PositiveBigIntegerField()
    extended_args = models.CharField(max_length=8000, blank=True, null=True)
    priority = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_actionscheduler_actions'


class WpActionschedulerClaims(models.Model):
    claim_id = models.BigAutoField(primary_key=True)
    date_created_gmt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_actionscheduler_claims'


class WpActionschedulerGroups(models.Model):
    group_id = models.BigAutoField(primary_key=True)
    slug = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wp_actionscheduler_groups'


class WpActionschedulerLogs(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    action_id = models.PositiveBigIntegerField()
    message = models.TextField()
    log_date_gmt = models.DateTimeField(blank=True, null=True)
    log_date_local = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_actionscheduler_logs'


class WpBvFwRequests(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.CharField(max_length=50)
    status = models.IntegerField()
    time = models.BigIntegerField()
    path = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    resp_code = models.IntegerField()
    category = models.IntegerField()
    referer = models.CharField(max_length=200)
    user_agent = models.CharField(max_length=200)
    filenames = models.TextField(blank=True, null=True)
    query_string = models.TextField(blank=True, null=True)
    rules_info = models.TextField(blank=True, null=True)
    request_id = models.CharField(max_length=200, blank=True, null=True)
    matched_rules = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_bv_fw_requests'


class WpBvIpStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_ip_range = models.CharField(max_length=16)
    end_ip_range = models.CharField(max_length=16)
    is_fw = models.IntegerField()
    is_lp = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bv_ip_store'


class WpBvLpRequests(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.CharField(max_length=50)
    status = models.IntegerField()
    username = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    category = models.IntegerField()
    time = models.BigIntegerField()
    request_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_bv_lp_requests'


class WpBwgAlbum(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()
    preview_image = models.TextField()
    random_preview_image = models.TextField()
    order = models.BigIntegerField()
    author = models.BigIntegerField()
    published = models.IntegerField()
    modified_date = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_album'


class WpBwgAlbumGallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    album_id = models.BigIntegerField()
    is_album = models.IntegerField()
    alb_gal_id = models.BigIntegerField()
    order = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_album_gallery'


class WpBwgFilePaths(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_dir = models.IntegerField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    filename = models.CharField(max_length=250, blank=True, null=True)
    alt = models.CharField(max_length=250, blank=True, null=True)
    thumb = models.CharField(max_length=250, blank=True, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)
    resolution = models.CharField(max_length=15, blank=True, null=True)
    resolution_thumb = models.CharField(max_length=15, blank=True, null=True)
    credit = models.CharField(max_length=250, blank=True, null=True)
    aperture = models.IntegerField(blank=True, null=True)
    camera = models.CharField(max_length=250, blank=True, null=True)
    caption = models.CharField(max_length=250, blank=True, null=True)
    iso = models.IntegerField(blank=True, null=True)
    orientation = models.IntegerField(blank=True, null=True)
    copyright = models.CharField(max_length=250, blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)
    author = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_bwg_file_paths'


class WpBwgGallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()
    page_link = models.TextField()
    preview_image = models.TextField()
    random_preview_image = models.TextField()
    order = models.BigIntegerField()
    author = models.BigIntegerField()
    published = models.IntegerField()
    gallery_type = models.CharField(max_length=32)
    gallery_source = models.CharField(max_length=256)
    autogallery_image_number = models.IntegerField()
    update_flag = models.CharField(max_length=32)
    modified_date = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_gallery'


class WpBwgImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    gallery_id = models.BigIntegerField()
    slug = models.TextField()
    filename = models.CharField(max_length=255)
    image_url = models.TextField()
    thumb_url = models.TextField()
    description = models.TextField()
    alt = models.TextField()
    date = models.CharField(max_length=128)
    size = models.CharField(max_length=128)
    filetype = models.CharField(max_length=128)
    resolution = models.CharField(max_length=128)
    resolution_thumb = models.CharField(max_length=128)
    author = models.BigIntegerField()
    order = models.BigIntegerField()
    published = models.IntegerField()
    comment_count = models.BigIntegerField()
    avg_rating = models.FloatField()
    rate_count = models.BigIntegerField()
    hit_count = models.BigIntegerField()
    redirect_url = models.CharField(max_length=255)
    pricelist_id = models.BigIntegerField()
    modified_date = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_image'


class WpBwgImageComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    date = models.CharField(max_length=64)
    comment = models.TextField()
    url = models.TextField()
    mail = models.TextField()
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_image_comment'


class WpBwgImageRate(models.Model):
    id = models.BigAutoField(primary_key=True)
    image_id = models.BigIntegerField()
    rate = models.FloatField()
    ip = models.CharField(max_length=64)
    date = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'wp_bwg_image_rate'


class WpBwgImageTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag_id = models.BigIntegerField()
    image_id = models.BigIntegerField()
    gallery_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_image_tag'


class WpBwgShortcode(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tagtext = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_shortcode'


class WpBwgTheme(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    options = models.TextField()
    default_theme = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_bwg_theme'


class WpCloudinaryRelationships(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.BigIntegerField(blank=True, null=True)
    public_id = models.CharField(max_length=1000, blank=True, null=True)
    parent_path = models.CharField(max_length=1000, blank=True, null=True)
    sized_url = models.CharField(max_length=1000, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=12, blank=True, null=True)
    sync_type = models.CharField(max_length=45, blank=True, null=True)
    post_state = models.CharField(max_length=12, blank=True, null=True)
    transformations = models.TextField(blank=True, null=True)
    signature = models.CharField(max_length=45, blank=True, null=True)
    public_hash = models.CharField(max_length=45, blank=True, null=True)
    url_hash = models.CharField(unique=True, max_length=45, blank=True, null=True)
    parent_hash = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_cloudinary_relationships'


class WpCommentmeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    comment_id = models.PositiveBigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_commentmeta'


class WpComments(models.Model):
    comment_id = models.BigAutoField(db_column='comment_ID', primary_key=True)  # Field name made lowercase.
    comment_post_id = models.PositiveBigIntegerField(db_column='comment_post_ID')  # Field name made lowercase.
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=100)
    comment_author_url = models.CharField(max_length=200)
    comment_author_ip = models.CharField(db_column='comment_author_IP', max_length=100)  # Field name made lowercase.
    comment_date = models.DateTimeField()
    comment_date_gmt = models.DateTimeField()
    comment_content = models.TextField()
    comment_karma = models.IntegerField()
    comment_approved = models.CharField(max_length=20)
    comment_agent = models.CharField(max_length=255)
    comment_type = models.CharField(max_length=20)
    comment_parent = models.PositiveBigIntegerField()
    user_id = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_comments'


class WpEEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_data = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_e_events'


class WpENotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    route_url = models.TextField(blank=True, null=True, db_comment='Clean url where the note was created.')
    route_title = models.CharField(max_length=255, blank=True, null=True)
    route_post_id = models.PositiveBigIntegerField(blank=True, null=True, db_comment='The post id of the route that the note was created on.')
    post_id = models.PositiveBigIntegerField(blank=True, null=True)
    element_id = models.CharField(max_length=60, blank=True, null=True, db_comment='The Elementor element ID the note is attached to.')
    parent_id = models.PositiveBigIntegerField()
    author_id = models.PositiveBigIntegerField(blank=True, null=True)
    author_display_name = models.CharField(max_length=250, blank=True, null=True, db_comment='Save the author name when the author was deleted.')
    status = models.CharField(max_length=20)
    position = models.TextField(blank=True, null=True, db_comment='A JSON string that represents the position of the note inside the element in percentages. e.g. {x:10, y:15}')
    content = models.TextField(blank=True, null=True)
    is_resolved = models.IntegerField()
    is_public = models.IntegerField()
    last_activity_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_e_notes'


class WpENotesUsersRelations(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=60, db_comment='The relation type between user and note (e.g mention, watch, read).')
    note_id = models.PositiveBigIntegerField()
    user_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_e_notes_users_relations'


class WpESubmissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=60, blank=True, null=True)
    hash_id = models.CharField(unique=True, max_length=60)
    main_meta_id = models.PositiveBigIntegerField(db_comment='Id of main field. to represent the main meta field')
    post_id = models.PositiveBigIntegerField()
    referer = models.CharField(max_length=500)
    referer_title = models.CharField(max_length=300, blank=True, null=True)
    element_id = models.CharField(max_length=20)
    form_name = models.CharField(max_length=60)
    campaign_id = models.PositiveBigIntegerField()
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    user_ip = models.CharField(max_length=46)
    user_agent = models.TextField()
    actions_count = models.IntegerField(blank=True, null=True)
    actions_succeeded_count = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20)
    is_read = models.IntegerField()
    meta = models.TextField(blank=True, null=True)
    created_at_gmt = models.DateTimeField()
    updated_at_gmt = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_e_submissions'


class WpESubmissionsActionsLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    submission_id = models.PositiveBigIntegerField()
    action_name = models.CharField(max_length=60)
    action_label = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=20)
    log = models.TextField(blank=True, null=True)
    created_at_gmt = models.DateTimeField()
    updated_at_gmt = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_e_submissions_actions_log'


class WpESubmissionsValues(models.Model):
    id = models.BigAutoField(primary_key=True)
    submission_id = models.PositiveBigIntegerField()
    key = models.CharField(max_length=60, blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_e_submissions_values'


class WpEwwwioImages(models.Model):
    id = models.AutoField(unique=True)
    attachment_id = models.PositiveBigIntegerField(blank=True, null=True)
    gallery = models.CharField(max_length=10, blank=True, null=True)
    resize = models.CharField(max_length=75, blank=True, null=True)
    path = models.TextField()
    converted = models.TextField()
    results = models.CharField(max_length=75)
    image_size = models.PositiveIntegerField(blank=True, null=True)
    orig_size = models.PositiveIntegerField(blank=True, null=True)
    backup = models.CharField(max_length=100, blank=True, null=True)
    level = models.PositiveIntegerField(blank=True, null=True)
    pending = models.IntegerField()
    updates = models.PositiveIntegerField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    trace = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_ewwwio_images'


class WpFgRedirect(models.Model):
    old_url = models.CharField(primary_key=True, max_length=255)
    id = models.PositiveBigIntegerField()
    type = models.CharField(max_length=20)
    activated = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_fg_redirect'


class WpGgAttributes(models.Model):
    pid = models.IntegerField()
    attributes = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_gg_attributes'


class WpGgGalleries(models.Model):
    title = models.CharField(max_length=255)
    settings_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_gg_galleries'


class WpGgGalleriesResources(models.Model):
    id = models.AutoField(unique=True)
    resource_type = models.CharField(max_length=6)
    resource_id = models.IntegerField()
    gallery_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_gg_galleries_resources'


class WpGgPhotos(models.Model):
    folder_id = models.IntegerField()
    album_id = models.IntegerField()
    attachment_id = models.IntegerField()
    position = models.IntegerField()
    timestamp = models.DateTimeField()
    link_type = models.IntegerField()
    link_full = models.CharField(max_length=255)
    link_thumb = models.CharField(max_length=255)
    link_default = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wp_gg_photos'


class WpGgSettingsSets(models.Model):
    data = models.TextField()
    gallery_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_gg_settings_sets'


class WpGgTags(models.Model):
    pid = models.IntegerField()
    tags = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wp_gg_tags'


class WpGmedia(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    author = models.PositiveBigIntegerField()
    date = models.DateTimeField()
    description = models.TextField()
    title = models.TextField()
    gmuid = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    modified = models.DateTimeField()
    mime_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    post_id = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_gmedia'


class WpGmediaLog(models.Model):
    log = models.CharField(max_length=200)
    id = models.PositiveBigIntegerField(db_column='ID')  # Field name made lowercase.
    log_author = models.PositiveBigIntegerField()
    log_date = models.DateTimeField()
    log_data = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'wp_gmedia_log'


class WpGmediaMeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    gmedia_id = models.PositiveBigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_gmedia_meta'


class WpGmediaTerm(models.Model):
    term_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    taxonomy = models.CharField(max_length=32)
    description = models.TextField()
    global_field = models.PositiveBigIntegerField(db_column='global')  # Field renamed because it was a Python reserved word.
    count = models.BigIntegerField()
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'wp_gmedia_term'


class WpGmediaTermMeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    gmedia_term_id = models.PositiveBigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_gmedia_term_meta'


class WpGmediaTermRelationships(models.Model):
    gmedia_id = models.PositiveBigIntegerField(primary_key=True)  # The composite primary key (gmedia_id, gmedia_term_id) found, that is not supported. The first column is selected.
    gmedia_term_id = models.PositiveBigIntegerField()
    term_order = models.IntegerField()
    gmedia_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_gmedia_term_relationships'
        unique_together = (('gmedia_id', 'gmedia_term_id'),)


class WpImagifyFiles(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    folder_id = models.PositiveBigIntegerField()
    file_date = models.DateTimeField()
    path = models.CharField(unique=True, max_length=191)
    hash = models.CharField(max_length=32)
    mime_type = models.CharField(max_length=100)
    modified = models.PositiveIntegerField()
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    original_size = models.PositiveIntegerField()
    optimized_size = models.PositiveIntegerField(blank=True, null=True)
    percent = models.PositiveSmallIntegerField(blank=True, null=True)
    optimization_level = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    error = models.CharField(max_length=255, blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_imagify_files'


class WpImagifyFolders(models.Model):
    folder_id = models.BigAutoField(primary_key=True)
    path = models.CharField(unique=True, max_length=191)
    active = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_imagify_folders'


class WpIntegrityCheckerFiles(models.Model):
    version = models.IntegerField()
    name = models.CharField(max_length=4096)
    hash = models.CharField(max_length=64, blank=True, null=True)
    modified = models.IntegerField(blank=True, null=True)
    found = models.IntegerField(blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)
    isdir = models.IntegerField()
    islink = models.IntegerField()
    size = models.BigIntegerField()
    mode = models.SmallIntegerField()
    fileowner = models.CharField(max_length=32, blank=True, null=True)
    filegroup = models.CharField(max_length=32, blank=True, null=True)
    mime = models.CharField(max_length=50)
    permissionsresult = models.SmallIntegerField(blank=True, null=True)
    status = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'wp_integrity_checker_files'


class WpItsecLockouts(models.Model):
    lockout_id = models.BigAutoField(primary_key=True)
    lockout_type = models.CharField(max_length=20)
    lockout_start = models.DateTimeField()
    lockout_start_gmt = models.DateTimeField()
    lockout_expire = models.DateTimeField()
    lockout_expire_gmt = models.DateTimeField()
    lockout_host = models.CharField(max_length=40, blank=True, null=True)
    lockout_user = models.PositiveBigIntegerField(blank=True, null=True)
    lockout_username = models.CharField(max_length=60, blank=True, null=True)
    lockout_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_itsec_lockouts'


class WpItsecLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    log_type = models.CharField(max_length=20)
    log_function = models.CharField(max_length=255)
    log_priority = models.IntegerField()
    log_date = models.DateTimeField()
    log_date_gmt = models.DateTimeField()
    log_host = models.CharField(max_length=40, blank=True, null=True)
    log_username = models.CharField(max_length=60, blank=True, null=True)
    log_user = models.PositiveBigIntegerField(blank=True, null=True)
    log_url = models.CharField(max_length=255, blank=True, null=True)
    log_referrer = models.CharField(max_length=255, blank=True, null=True)
    log_data = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_itsec_log'


class WpItsecTemp(models.Model):
    temp_id = models.BigAutoField(primary_key=True)
    temp_type = models.CharField(max_length=20)
    temp_date = models.DateTimeField()
    temp_date_gmt = models.DateTimeField()
    temp_host = models.CharField(max_length=40, blank=True, null=True)
    temp_user = models.PositiveBigIntegerField(blank=True, null=True)
    temp_username = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_itsec_temp'


class WpJnewsPostLike(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.IntegerField()
    date_time = models.DateTimeField()
    value = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_jnews_post_like'


class WpLinks(models.Model):
    link_id = models.BigAutoField(primary_key=True)
    link_url = models.CharField(max_length=255)
    link_name = models.CharField(max_length=255)
    link_image = models.CharField(max_length=255)
    link_target = models.CharField(max_length=25)
    link_description = models.CharField(max_length=255)
    link_visible = models.CharField(max_length=20)
    link_owner = models.PositiveBigIntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=255)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wp_links'


class WpNewRoyalsliders(models.Model):
    active = models.IntegerField()
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    skin = models.CharField(max_length=100)
    template = models.CharField(max_length=100)
    slides = models.TextField()
    options = models.TextField()
    template_html = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_new_royalsliders'


class WpNf3ActionMeta(models.Model):
    id = models.AutoField(unique=True)
    parent_id = models.IntegerField()
    key = models.TextField()
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_action_meta'


class WpNf3Actions(models.Model):
    id = models.AutoField(unique=True)
    title = models.TextField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_actions'


class WpNf3Chunks(models.Model):
    id = models.AutoField(unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_chunks'


class WpNf3FieldMeta(models.Model):
    id = models.AutoField(unique=True)
    parent_id = models.IntegerField()
    key = models.TextField()
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_field_meta'


class WpNf3Fields(models.Model):
    id = models.AutoField(unique=True)
    label = models.TextField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    parent_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_fields'


class WpNf3FormMeta(models.Model):
    id = models.AutoField(unique=True)
    parent_id = models.IntegerField()
    key = models.TextField()
    value = models.TextField(blank=True, null=True)
    meta_key = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    meta_value = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_form_meta'


class WpNf3Forms(models.Model):
    id = models.AutoField(unique=True)
    title = models.TextField(blank=True, null=True)
    key = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    subs = models.IntegerField(blank=True, null=True)
    form_title = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    default_label_pos = models.CharField(max_length=15, db_collation='utf8mb4_general_ci', blank=True, null=True)
    show_title = models.TextField(blank=True, null=True)  # This field type is a guess.
    clear_complete = models.TextField(blank=True, null=True)  # This field type is a guess.
    hide_complete = models.TextField(blank=True, null=True)  # This field type is a guess.
    logged_in = models.TextField(blank=True, null=True)  # This field type is a guess.
    seq_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_forms'


class WpNf3ObjectMeta(models.Model):
    id = models.AutoField(unique=True)
    parent_id = models.IntegerField()
    key = models.TextField()
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_object_meta'


class WpNf3Objects(models.Model):
    id = models.AutoField(unique=True)
    type = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_objects'


class WpNf3Relationships(models.Model):
    id = models.AutoField(unique=True)
    child_id = models.IntegerField()
    child_type = models.TextField()
    parent_id = models.IntegerField()
    parent_type = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_nf3_relationships'


class WpNf3Upgrades(models.Model):
    id = models.IntegerField(primary_key=True)
    cache = models.TextField(blank=True, null=True)
    stage = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_nf3_upgrades'


class WpNggAlbum(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    previewpic = models.BigIntegerField()
    albumdesc = models.TextField(blank=True, null=True)
    sortorder = models.TextField()
    pageid = models.BigIntegerField()
    extras_post_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_ngg_album'


class WpNggGallery(models.Model):
    gid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    path = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    galdesc = models.TextField(blank=True, null=True)
    pageid = models.BigIntegerField()
    previewpic = models.BigIntegerField()
    author = models.BigIntegerField()
    extras_post_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_ngg_gallery'


class WpNggPictures(models.Model):
    pid = models.BigAutoField(primary_key=True)
    image_slug = models.CharField(max_length=255)
    post_id = models.BigIntegerField()
    galleryid = models.BigIntegerField()
    filename = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    alttext = models.TextField(blank=True, null=True)
    imagedate = models.DateTimeField()
    exclude = models.IntegerField(blank=True, null=True)
    sortorder = models.BigIntegerField()
    meta_data = models.TextField(blank=True, null=True)
    extras_post_id = models.BigIntegerField()
    updated_at = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_ngg_pictures'


class WpOptions(models.Model):
    option_id = models.BigAutoField(primary_key=True)
    option_name = models.CharField(unique=True, max_length=191)
    option_value = models.TextField()
    autoload = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'wp_options'


class WpPmxeExports(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent_id = models.BigIntegerField()
    attch_id = models.BigIntegerField()
    options = models.TextField(blank=True, null=True)
    scheduled = models.CharField(max_length=64)
    registered_on = models.DateTimeField()
    friendly_name = models.CharField(max_length=64)
    exported = models.BigIntegerField()
    canceled = models.IntegerField()
    canceled_on = models.DateTimeField()
    settings_update_on = models.DateTimeField()
    last_activity = models.DateTimeField()
    processing = models.IntegerField()
    executing = models.IntegerField()
    triggered = models.IntegerField()
    iteration = models.BigIntegerField()
    export_post_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'wp_pmxe_exports'


class WpPmxeGoogleCats(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    parent_id = models.IntegerField()
    parent_name = models.CharField(max_length=200)
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_pmxe_google_cats'


class WpPmxePosts(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.PositiveBigIntegerField()
    export_id = models.PositiveBigIntegerField()
    iteration = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_pmxe_posts'


class WpPmxeTemplates(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    options = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_pmxe_templates'


class WpPmxiFiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    import_id = models.PositiveBigIntegerField()
    name = models.TextField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    registered_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_pmxi_files'


class WpPmxiHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    import_id = models.PositiveBigIntegerField()
    type = models.CharField(max_length=10)
    time_run = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    summary = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_pmxi_history'


class WpPmxiImages(models.Model):
    id = models.BigAutoField(primary_key=True)
    attachment_id = models.PositiveBigIntegerField()
    image_url = models.CharField(max_length=600)
    image_filename = models.CharField(max_length=600)

    class Meta:
        managed = False
        db_table = 'wp_pmxi_images'


class WpPmxiImports(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent_import_id = models.BigIntegerField()
    name = models.TextField(blank=True, null=True)
    friendly_name = models.CharField(max_length=255)
    type = models.CharField(max_length=32)
    feed_type = models.CharField(max_length=3)
    path = models.TextField(blank=True, null=True)
    xpath = models.TextField(blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    registered_on = models.DateTimeField()
    root_element = models.CharField(max_length=255, blank=True, null=True)
    processing = models.IntegerField()
    executing = models.IntegerField()
    triggered = models.IntegerField()
    queue_chunk_number = models.BigIntegerField()
    first_import = models.DateTimeField()
    count = models.BigIntegerField()
    imported = models.BigIntegerField()
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    skipped = models.BigIntegerField()
    deleted = models.BigIntegerField()
    canceled = models.IntegerField()
    canceled_on = models.DateTimeField()
    failed = models.IntegerField()
    failed_on = models.DateTimeField()
    settings_update_on = models.DateTimeField()
    last_activity = models.DateTimeField()
    iteration = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_pmxi_imports'


class WpPmxiPosts(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.PositiveBigIntegerField()
    import_id = models.PositiveBigIntegerField()
    unique_key = models.TextField(blank=True, null=True)
    product_key = models.TextField(blank=True, null=True)
    iteration = models.BigIntegerField()
    specified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_pmxi_posts'


class WpPmxiTemplates(models.Model):
    id = models.BigAutoField(primary_key=True)
    options = models.TextField(blank=True, null=True)
    scheduled = models.CharField(max_length=64)
    name = models.CharField(max_length=200)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_keep_linebreaks = models.IntegerField()
    is_leave_html = models.IntegerField()
    fix_characters = models.IntegerField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_pmxi_templates'


class WpPopularpostsdata(models.Model):
    postid = models.BigIntegerField(primary_key=True)
    day = models.DateTimeField()
    last_viewed = models.DateTimeField()
    pageviews = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_popularpostsdata'


class WpPopularpostssummary(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    postid = models.BigIntegerField()
    pageviews = models.BigIntegerField()
    view_date = models.DateField()
    view_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_popularpostssummary'


class WpPostmeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    post_id = models.PositiveBigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_postmeta'


class WpPosts(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    post_author = models.PositiveBigIntegerField()
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=20)
    comment_status = models.CharField(max_length=20)
    ping_status = models.CharField(max_length=20)
    post_password = models.CharField(max_length=255)
    post_name = models.CharField(max_length=3000)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.PositiveBigIntegerField()
    guid = models.CharField(max_length=255)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=20)
    post_mime_type = models.CharField(max_length=100)
    comment_count = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_posts'


class WpRankMath404Logs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uri = models.CharField(max_length=255)
    accessed = models.DateTimeField()
    times_accessed = models.PositiveBigIntegerField()
    referer = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wp_rank_math_404_logs'


class WpRankMathAnalyticsGsc(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    query = models.CharField(max_length=1000)
    page = models.CharField(max_length=500)
    clicks = models.IntegerField()
    impressions = models.IntegerField()
    position = models.FloatField()
    ctr = models.FloatField()

    class Meta:
        managed = False
        db_table = 'wp_rank_math_analytics_gsc'


class WpRankMathAnalyticsInspections(models.Model):
    id = models.BigAutoField(primary_key=True)
    page = models.CharField(max_length=500)
    created = models.DateTimeField()
    index_verdict = models.CharField(max_length=64)
    indexing_state = models.CharField(max_length=64)
    coverage_state = models.TextField()
    page_fetch_state = models.CharField(max_length=64)
    robots_txt_state = models.CharField(max_length=64)
    mobile_usability_verdict = models.CharField(max_length=64)
    mobile_usability_issues = models.TextField()
    rich_results_verdict = models.CharField(max_length=64)
    rich_results_items = models.TextField()
    last_crawl_time = models.DateTimeField()
    crawled_as = models.CharField(max_length=64)
    google_canonical = models.TextField()
    user_canonical = models.TextField()
    sitemap = models.TextField()
    referring_urls = models.TextField()
    raw_api_response = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_rank_math_analytics_inspections'


class WpRankMathAnalyticsKeywordManager(models.Model):
    id = models.BigAutoField(primary_key=True)
    keyword = models.CharField(max_length=1000)
    collection = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_rank_math_analytics_keyword_manager'


class WpRankMathAnalyticsObjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField()
    title = models.TextField()
    page = models.CharField(max_length=500)
    object_type = models.CharField(max_length=100)
    object_subtype = models.CharField(max_length=100)
    object_id = models.PositiveBigIntegerField()
    primary_key = models.CharField(max_length=255)
    seo_score = models.IntegerField()
    page_score = models.IntegerField()
    is_indexable = models.IntegerField()
    schemas_in_use = models.CharField(max_length=500, blank=True, null=True)
    desktop_interactive = models.FloatField(blank=True, null=True)
    desktop_pagescore = models.FloatField(blank=True, null=True)
    mobile_interactive = models.FloatField(blank=True, null=True)
    mobile_pagescore = models.FloatField(blank=True, null=True)
    pagespeed_refreshed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_rank_math_analytics_objects'


class WpRankMathInternalLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=255)
    post_id = models.PositiveBigIntegerField()
    target_post_id = models.PositiveBigIntegerField()
    type = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'wp_rank_math_internal_links'


class WpRankMathInternalMeta(models.Model):
    object_id = models.PositiveBigIntegerField(primary_key=True)
    internal_link_count = models.PositiveIntegerField(blank=True, null=True)
    external_link_count = models.PositiveIntegerField(blank=True, null=True)
    incoming_link_count = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_rank_math_internal_meta'


class WpRankMathRedirections(models.Model):
    id = models.BigAutoField(primary_key=True)
    sources = models.TextField(db_collation='utf8mb4_bin')
    url_to = models.TextField()
    header_code = models.PositiveSmallIntegerField()
    hits = models.PositiveBigIntegerField()
    status = models.CharField(max_length=25)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    last_accessed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_rank_math_redirections'


class WpRankMathRedirectionsCache(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_url = models.TextField(db_collation='utf8mb4_bin')
    redirection_id = models.PositiveBigIntegerField()
    object_id = models.PositiveBigIntegerField()
    object_type = models.CharField(max_length=10)
    is_redirected = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_rank_math_redirections_cache'


class WpRevsliderCss(models.Model):
    id = models.AutoField(unique=True)
    handle = models.TextField()
    settings = models.TextField(blank=True, null=True)
    hover = models.TextField(blank=True, null=True)
    advanced = models.TextField(blank=True, null=True)
    params = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_revslider_css'


class WpRevsliderLayerAnimations(models.Model):
    id = models.AutoField(unique=True)
    handle = models.TextField()
    params = models.TextField()
    settings = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_revslider_layer_animations'


class WpRevsliderNavigations(models.Model):
    id = models.AutoField(unique=True)
    name = models.CharField(max_length=191)
    handle = models.CharField(max_length=191)
    css = models.TextField()
    markup = models.TextField()
    settings = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_revslider_navigations'


class WpRevsliderSliders(models.Model):
    id = models.AutoField(unique=True)
    title = models.TextField()
    alias = models.TextField(blank=True, null=True)
    params = models.TextField()
    settings = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'wp_revslider_sliders'


class WpRevsliderSlides(models.Model):
    id = models.AutoField(unique=True)
    slider_id = models.IntegerField()
    slide_order = models.IntegerField()
    params = models.TextField()
    layers = models.TextField()
    settings = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_revslider_slides'


class WpRevsliderStaticSlides(models.Model):
    id = models.AutoField(unique=True)
    slider_id = models.IntegerField()
    params = models.TextField()
    layers = models.TextField()
    settings = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_revslider_static_slides'


class WpShortpixelCriticalCssApiQueue(models.Model):
    template = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_critical_css_api_queue'


class WpShortpixelCriticalCssProcessedItems(models.Model):
    template = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_critical_css_processed_items'


class WpShortpixelCriticalCssTemplateLog(models.Model):
    template = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_critical_css_template_log'


class WpShortpixelCriticalCssWebCheckQueue(models.Model):
    template = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_critical_css_web_check_queue'


class WpShortpixelFolders(models.Model):
    path = models.CharField(max_length=512, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    path_md5 = models.CharField(max_length=32, blank=True, null=True)
    file_count = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField()
    ts_updated = models.DateTimeField()
    ts_created = models.DateTimeField()
    parent = models.SmallIntegerField(blank=True, null=True)
    ts_checked = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_folders'


class WpShortpixelMeta(models.Model):
    folder_id = models.IntegerField()
    ext_meta_id = models.IntegerField(blank=True, null=True)
    path = models.CharField(max_length=512, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    path_md5 = models.CharField(max_length=32, blank=True, null=True)
    compressed_size = models.IntegerField()
    compression_type = models.IntegerField(blank=True, null=True)
    keep_exif = models.IntegerField(blank=True, null=True)
    cmyk2rgb = models.IntegerField(blank=True, null=True)
    resize = models.IntegerField(blank=True, null=True)
    resize_width = models.SmallIntegerField(blank=True, null=True)
    resize_height = models.SmallIntegerField(blank=True, null=True)
    backup = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField()
    retries = models.IntegerField()
    message = models.CharField(max_length=255, blank=True, null=True)
    ts_added = models.DateTimeField()
    ts_optimized = models.DateTimeField()
    extra_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_meta'


class WpShortpixelPostmeta(models.Model):
    id = models.BigAutoField(primary_key=True)
    attach_id = models.PositiveBigIntegerField()
    parent = models.PositiveBigIntegerField()
    image_type = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    compression_type = models.IntegerField(blank=True, null=True)
    compressed_size = models.IntegerField(blank=True, null=True)
    original_size = models.IntegerField(blank=True, null=True)
    tsadded = models.DateTimeField(db_column='tsAdded')  # Field name made lowercase.
    tsoptimized = models.DateTimeField(db_column='tsOptimized')  # Field name made lowercase.
    extra_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_postmeta'


class WpShortpixelQueue(models.Model):
    queue_name = models.CharField(max_length=30)
    plugin_slug = models.CharField(max_length=30)
    status = models.IntegerField()
    list_order = models.IntegerField()
    item_id = models.PositiveBigIntegerField()
    item_count = models.IntegerField(blank=True, null=True)
    value = models.TextField()
    tries = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_shortpixel_queue'
        unique_together = (('plugin_slug', 'queue_name', 'item_id'),)


class WpSmushDirImages(models.Model):
    id = models.AutoField(unique=True)
    path = models.TextField()
    path_hash = models.CharField(unique=True, max_length=32, blank=True, null=True)
    resize = models.CharField(max_length=55, blank=True, null=True)
    lossy = models.CharField(max_length=55, blank=True, null=True)
    error = models.CharField(max_length=55, blank=True, null=True)
    image_size = models.PositiveIntegerField(blank=True, null=True)
    orig_size = models.PositiveIntegerField(blank=True, null=True)
    file_time = models.PositiveIntegerField(blank=True, null=True)
    last_scan = models.DateTimeField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_smush_dir_images'


class WpTermRelationships(models.Model):
    object_id = models.PositiveBigIntegerField(primary_key=True)  # The composite primary key (object_id, term_taxonomy_id) found, that is not supported. The first column is selected.
    term_taxonomy_id = models.PositiveBigIntegerField()
    term_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_term_relationships'
        unique_together = (('object_id', 'term_taxonomy_id'),)


class WpTermTaxonomy(models.Model):
    term_taxonomy_id = models.BigAutoField(primary_key=True)
    term_id = models.PositiveBigIntegerField()
    taxonomy = models.CharField(max_length=32)
    description = models.TextField()
    parent = models.PositiveBigIntegerField()
    count = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_term_taxonomy'
        unique_together = (('term_id', 'taxonomy'),)


class WpTermmeta(models.Model):
    meta_id = models.BigAutoField(primary_key=True)
    term_id = models.PositiveBigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_termmeta'


class WpTerms(models.Model):
    term_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    term_group = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_terms'


class WpToolsetPostGuidId(models.Model):
    guid = models.CharField(max_length=190)
    post_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'wp_toolset_post_guid_id'


class WpUsermeta(models.Model):
    umeta_id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True, null=True)
    meta_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_usermeta'


class WpUsers(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user_login = models.CharField(max_length=60)
    user_pass = models.CharField(max_length=255)
    user_nicename = models.CharField(max_length=50)
    user_email = models.CharField(max_length=100)
    user_url = models.CharField(max_length=100)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=255)
    user_status = models.IntegerField()
    display_name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'wp_users'


class WpWdslayer(models.Model):
    title = models.TextField()
    slide_id = models.BigIntegerField()
    type = models.CharField(max_length=8)
    depth = models.BigIntegerField()
    text = models.TextField()
    link = models.TextField()
    left = models.IntegerField()
    top = models.IntegerField()
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    published = models.IntegerField()
    color = models.CharField(max_length=8)
    size = models.BigIntegerField()
    ffamily = models.CharField(max_length=32)
    fweight = models.CharField(max_length=8)
    padding = models.CharField(max_length=32)
    fbgcolor = models.CharField(max_length=8)
    transparent = models.IntegerField()
    border_width = models.IntegerField()
    border_style = models.CharField(max_length=16)
    border_color = models.CharField(max_length=8)
    border_radius = models.CharField(max_length=32)
    shadow = models.CharField(max_length=127)
    image_url = models.TextField()
    image_width = models.IntegerField()
    image_height = models.IntegerField()
    image_scale = models.CharField(max_length=8)
    alt = models.CharField(max_length=127)
    imgtransparent = models.IntegerField()
    social_button = models.CharField(max_length=16)
    hover_color = models.CharField(max_length=8)
    layer_effect_in = models.CharField(max_length=32)
    duration_eff_in = models.BigIntegerField()
    layer_effect_out = models.CharField(max_length=32)
    duration_eff_out = models.BigIntegerField()
    target_attr_layer = models.IntegerField()
    hotp_width = models.IntegerField()
    hotp_fbgcolor = models.CharField(max_length=8)
    hotp_border_width = models.IntegerField()
    hotp_border_style = models.CharField(max_length=16)
    hotp_border_color = models.CharField(max_length=8)
    hotp_border_radius = models.CharField(max_length=32)
    hotp_text_position = models.CharField(max_length=6)
    google_fonts = models.IntegerField()
    add_class = models.CharField(max_length=127)
    layer_video_loop = models.IntegerField()
    youtube_rel_layer_video = models.IntegerField()
    hotspot_animation = models.IntegerField()
    layer_callback_list = models.CharField(max_length=32)
    hotspot_text_display = models.CharField(max_length=8)
    hover_color_text = models.CharField(max_length=8)
    text_alignment = models.CharField(max_length=8)
    link_to_slide = models.IntegerField()
    align_layer = models.IntegerField()
    static_layer = models.IntegerField()
    infinite_in = models.IntegerField()
    infinite_out = models.IntegerField()
    min_size = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wdslayer'


class WpWdsslide(models.Model):
    slider_id = models.BigIntegerField()
    title = models.TextField()
    type = models.CharField(max_length=128)
    image_url = models.TextField()
    thumb_url = models.TextField()
    published = models.IntegerField()
    link = models.TextField()
    order = models.BigIntegerField()
    target_attr_slide = models.IntegerField()
    youtube_rel_video = models.IntegerField()
    video_loop = models.IntegerField()
    fillmode = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'wp_wdsslide'


class WpWdsslider(models.Model):
    name = models.CharField(max_length=127)
    published = models.IntegerField()
    full_width = models.IntegerField()
    auto_height = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    align = models.CharField(max_length=8)
    effect = models.CharField(max_length=16)
    time_intervval = models.IntegerField()
    autoplay = models.IntegerField()
    shuffle = models.IntegerField()
    music = models.IntegerField()
    music_url = models.TextField()
    preload_images = models.IntegerField()
    background_color = models.CharField(max_length=8)
    background_transparent = models.IntegerField()
    glb_border_width = models.IntegerField()
    glb_border_style = models.CharField(max_length=16)
    glb_border_color = models.CharField(max_length=8)
    glb_border_radius = models.CharField(max_length=32)
    glb_margin = models.IntegerField()
    glb_box_shadow = models.CharField(max_length=127)
    image_right_click = models.IntegerField()
    layer_out_next = models.IntegerField()
    prev_next_butt = models.IntegerField()
    play_paus_butt = models.IntegerField()
    navigation = models.CharField(max_length=16)
    rl_butt_style = models.CharField(max_length=16)
    rl_butt_size = models.IntegerField()
    pp_butt_size = models.IntegerField()
    butts_color = models.CharField(max_length=8)
    butts_transparent = models.IntegerField()
    hover_color = models.CharField(max_length=8)
    nav_border_width = models.IntegerField()
    nav_border_style = models.CharField(max_length=16)
    nav_border_color = models.CharField(max_length=8)
    nav_border_radius = models.CharField(max_length=32)
    nav_bg_color = models.CharField(max_length=8)
    bull_position = models.CharField(max_length=16)
    bull_style = models.CharField(max_length=20)
    bull_size = models.IntegerField()
    bull_color = models.CharField(max_length=8)
    bull_act_color = models.CharField(max_length=8)
    bull_margin = models.IntegerField()
    film_pos = models.CharField(max_length=16)
    film_thumb_width = models.IntegerField()
    film_thumb_height = models.IntegerField()
    film_bg_color = models.CharField(max_length=8)
    film_tmb_margin = models.IntegerField()
    film_act_border_width = models.IntegerField()
    film_act_border_style = models.CharField(max_length=16)
    film_act_border_color = models.CharField(max_length=8)
    film_dac_transparent = models.IntegerField()
    built_in_watermark_type = models.CharField(max_length=16)
    built_in_watermark_position = models.CharField(max_length=16)
    built_in_watermark_size = models.IntegerField()
    built_in_watermark_url = models.TextField()
    built_in_watermark_text = models.TextField()
    built_in_watermark_font_size = models.IntegerField()
    built_in_watermark_font = models.CharField(max_length=16)
    built_in_watermark_color = models.CharField(max_length=8)
    built_in_watermark_opacity = models.IntegerField()
    css = models.TextField()
    timer_bar_type = models.CharField(max_length=16)
    timer_bar_size = models.IntegerField()
    timer_bar_color = models.CharField(max_length=8)
    timer_bar_transparent = models.IntegerField()
    spider_uploader = models.IntegerField()
    stop_animation = models.IntegerField()
    right_butt_url = models.CharField(max_length=255)
    left_butt_url = models.CharField(max_length=255)
    right_butt_hov_url = models.CharField(max_length=255)
    left_butt_hov_url = models.CharField(max_length=255)
    rl_butt_img_or_not = models.CharField(max_length=8)
    bullets_img_main_url = models.CharField(max_length=255)
    bullets_img_hov_url = models.CharField(max_length=255)
    bull_butt_img_or_not = models.CharField(max_length=8)
    play_paus_butt_img_or_not = models.CharField(max_length=8)
    play_butt_url = models.CharField(max_length=255)
    play_butt_hov_url = models.CharField(max_length=255)
    paus_butt_url = models.CharField(max_length=255)
    paus_butt_hov_url = models.CharField(max_length=255)
    start_slide_num = models.IntegerField()
    effect_duration = models.IntegerField()
    carousel = models.IntegerField()
    carousel_image_counts = models.IntegerField()
    carousel_image_parameters = models.CharField(max_length=8)
    carousel_fit_containerwidth = models.IntegerField(db_column='carousel_fit_containerWidth')  # Field name made lowercase.
    carousel_width = models.IntegerField()
    parallax_effect = models.IntegerField()
    mouse_swipe_nav = models.IntegerField()
    bull_hover = models.IntegerField()
    touch_swipe_nav = models.IntegerField()
    mouse_wheel_nav = models.IntegerField()
    keyboard_nav = models.IntegerField()
    possib_add_ffamily = models.CharField(max_length=255)
    show_thumbnail = models.IntegerField()
    thumb_size = models.CharField(max_length=8)
    fixed_bg = models.IntegerField()
    smart_crop = models.IntegerField()
    crop_image_position = models.CharField(max_length=16)
    javascript = models.TextField()
    carousel_degree = models.IntegerField()
    carousel_grayscale = models.IntegerField()
    carousel_transparency = models.IntegerField()
    bull_back_act_color = models.CharField(max_length=8)
    bull_back_color = models.CharField(max_length=8)
    bull_radius = models.CharField(max_length=32)
    possib_add_google_fonts = models.IntegerField()
    possib_add_ffamily_google = models.CharField(max_length=255)
    slider_loop = models.IntegerField()
    hide_on_mobile = models.IntegerField()
    twoway_slideshow = models.IntegerField()
    full_width_for_mobile = models.IntegerField()
    order_dir = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'wp_wdsslider'


class WpWfblockediplog(models.Model):
    ip = models.CharField(db_column='IP', primary_key=True, max_length=16)  # Field name made lowercase. The composite primary key (IP, unixday, blockType) found, that is not supported. The first column is selected.
    countrycode = models.CharField(db_column='countryCode', max_length=2)  # Field name made lowercase.
    blockcount = models.PositiveIntegerField(db_column='blockCount')  # Field name made lowercase.
    unixday = models.PositiveIntegerField()
    blocktype = models.CharField(db_column='blockType', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_wfBlockedIPLog'
        unique_together = (('ip', 'unixday', 'blocktype'),)


class WpWfblocks7(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.PositiveIntegerField()
    ip = models.CharField(db_column='IP', max_length=16)  # Field name made lowercase.
    blockedtime = models.BigIntegerField(db_column='blockedTime')  # Field name made lowercase.
    reason = models.CharField(max_length=255)
    lastattempt = models.PositiveIntegerField(db_column='lastAttempt', blank=True, null=True)  # Field name made lowercase.
    blockedhits = models.PositiveIntegerField(db_column='blockedHits', blank=True, null=True)  # Field name made lowercase.
    expiration = models.PositiveBigIntegerField()
    parameters = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_wfBlocks7'


class WpWfconfig(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    val = models.TextField(blank=True, null=True)
    autoload = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'wp_wfConfig'


class WpWfcrawlers(models.Model):
    ip = models.CharField(db_column='IP', primary_key=True, max_length=16)  # Field name made lowercase. The composite primary key (IP, patternSig) found, that is not supported. The first column is selected.
    patternsig = models.CharField(db_column='patternSig', max_length=16)  # Field name made lowercase.
    status = models.CharField(max_length=8)
    lastupdate = models.PositiveIntegerField(db_column='lastUpdate')  # Field name made lowercase.
    ptr = models.CharField(db_column='PTR', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_wfCrawlers'
        unique_together = (('ip', 'patternsig'),)


class WpWffilechanges(models.Model):
    filenamehash = models.CharField(db_column='filenameHash', primary_key=True, max_length=64)  # Field name made lowercase.
    file = models.CharField(max_length=1000)
    md5 = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'wp_wfFileChanges'


class WpWffilemods(models.Model):
    filenamemd5 = models.CharField(db_column='filenameMD5', primary_key=True, max_length=16)  # Field name made lowercase.
    filename = models.CharField(max_length=1000)
    real_path = models.TextField()
    knownfile = models.PositiveIntegerField(db_column='knownFile')  # Field name made lowercase.
    oldmd5 = models.CharField(db_column='oldMD5', max_length=16)  # Field name made lowercase.
    newmd5 = models.CharField(db_column='newMD5', max_length=16)  # Field name made lowercase.
    shac = models.CharField(db_column='SHAC', max_length=32)  # Field name made lowercase.
    stoppedonsignature = models.CharField(db_column='stoppedOnSignature', max_length=255)  # Field name made lowercase.
    stoppedonposition = models.PositiveIntegerField(db_column='stoppedOnPosition')  # Field name made lowercase.
    issafefile = models.CharField(db_column='isSafeFile', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_wfFileMods'


class WpWfhits(models.Model):
    attacklogtime = models.FloatField(db_column='attackLogTime')  # Field name made lowercase.
    ctime = models.FloatField()
    ip = models.CharField(db_column='IP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jsrun = models.IntegerField(db_column='jsRun', blank=True, null=True)  # Field name made lowercase.
    statuscode = models.IntegerField(db_column='statusCode')  # Field name made lowercase.
    isgoogle = models.IntegerField(db_column='isGoogle')  # Field name made lowercase.
    userid = models.PositiveIntegerField(db_column='userID')  # Field name made lowercase.
    newvisit = models.PositiveIntegerField(db_column='newVisit')  # Field name made lowercase.
    url = models.TextField(db_column='URL', blank=True, null=True)  # Field name made lowercase.
    referer = models.TextField(blank=True, null=True)
    ua = models.TextField(db_column='UA', blank=True, null=True)  # Field name made lowercase.
    action = models.CharField(max_length=64)
    actiondescription = models.TextField(db_column='actionDescription', blank=True, null=True)  # Field name made lowercase.
    actiondata = models.TextField(db_column='actionData', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_wfHits'


class WpWfhoover(models.Model):
    owner = models.TextField(blank=True, null=True)
    host = models.TextField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    hostkey = models.CharField(db_column='hostKey', max_length=124, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_wfHoover'


class WpWfissues(models.Model):
    time = models.PositiveIntegerField()
    lastupdated = models.PositiveIntegerField(db_column='lastUpdated')  # Field name made lowercase.
    status = models.CharField(max_length=10)
    type = models.CharField(max_length=20)
    severity = models.PositiveIntegerField()
    ignorep = models.CharField(db_column='ignoreP', max_length=32)  # Field name made lowercase.
    ignorec = models.CharField(db_column='ignoreC', max_length=32)  # Field name made lowercase.
    shortmsg = models.CharField(db_column='shortMsg', max_length=255)  # Field name made lowercase.
    longmsg = models.TextField(db_column='longMsg', blank=True, null=True)  # Field name made lowercase.
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_wfIssues'


class WpWfknownfilelist(models.Model):
    path = models.TextField()
    wordpress_path = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_wfKnownFileList'


class WpWflivetraffichuman(models.Model):
    ip = models.CharField(db_column='IP', primary_key=True, max_length=16)  # Field name made lowercase. The composite primary key (IP, identifier) found, that is not supported. The first column is selected.
    identifier = models.CharField(max_length=32)
    expiration = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wfLiveTrafficHuman'
        unique_together = (('ip', 'identifier'),)


class WpWflocs(models.Model):
    ip = models.CharField(db_column='IP', primary_key=True, max_length=16)  # Field name made lowercase.
    ctime = models.PositiveIntegerField()
    failed = models.PositiveIntegerField()
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    countryname = models.CharField(db_column='countryName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    countrycode = models.CharField(db_column='countryCode', max_length=2, blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_wfLocs'


class WpWflogins(models.Model):
    hitid = models.IntegerField(db_column='hitID', blank=True, null=True)  # Field name made lowercase.
    ctime = models.FloatField()
    fail = models.PositiveIntegerField()
    action = models.CharField(max_length=40)
    username = models.CharField(max_length=255)
    userid = models.PositiveIntegerField(db_column='userID')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    ua = models.TextField(db_column='UA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_wfLogins'


class WpWfnotifications(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    new = models.PositiveIntegerField()
    category = models.CharField(max_length=255)
    priority = models.IntegerField()
    ctime = models.PositiveIntegerField()
    html = models.TextField()
    links = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_wfNotifications'


class WpWfpendingissues(models.Model):
    time = models.PositiveIntegerField()
    lastupdated = models.PositiveIntegerField(db_column='lastUpdated')  # Field name made lowercase.
    status = models.CharField(max_length=10)
    type = models.CharField(max_length=20)
    severity = models.PositiveIntegerField()
    ignorep = models.CharField(db_column='ignoreP', max_length=32)  # Field name made lowercase.
    ignorec = models.CharField(db_column='ignoreC', max_length=32)  # Field name made lowercase.
    shortmsg = models.CharField(db_column='shortMsg', max_length=255)  # Field name made lowercase.
    longmsg = models.TextField(db_column='longMsg', blank=True, null=True)  # Field name made lowercase.
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_wfPendingIssues'


class WpWfreversecache(models.Model):
    ip = models.CharField(db_column='IP', primary_key=True, max_length=16)  # Field name made lowercase.
    host = models.CharField(max_length=255)
    lastupdate = models.PositiveIntegerField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wp_wfReverseCache'


class WpWfsnipcache(models.Model):
    ip = models.CharField(db_column='IP', max_length=45)  # Field name made lowercase.
    expiration = models.DateTimeField()
    body = models.CharField(max_length=255)
    count = models.PositiveIntegerField()
    type = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wfSNIPCache'


class WpWfsecurityevents(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=255)
    data = models.TextField()
    event_time = models.FloatField()
    state = models.CharField(max_length=7)
    state_timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_wfSecurityEvents'


class WpWfstatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    ctime = models.FloatField()
    level = models.PositiveIntegerField()
    type = models.CharField(max_length=5)
    msg = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'wp_wfStatus'


class WpWftrafficrates(models.Model):
    emin = models.PositiveIntegerField(db_column='eMin', primary_key=True)  # Field name made lowercase. The composite primary key (eMin, IP, hitType) found, that is not supported. The first column is selected.
    ip = models.CharField(db_column='IP', max_length=16)  # Field name made lowercase.
    hittype = models.CharField(db_column='hitType', max_length=3)  # Field name made lowercase.
    hits = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wfTrafficRates'
        unique_together = (('emin', 'ip', 'hittype'),)


class WpWfwaffailures(models.Model):
    throwable = models.TextField()
    rule_id = models.PositiveIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_wfWafFailures'


class WpWfls2FaSecrets(models.Model):
    user_id = models.PositiveBigIntegerField()
    secret = models.TextField()
    recovery = models.TextField()
    ctime = models.PositiveIntegerField()
    vtime = models.PositiveIntegerField()
    mode = models.CharField(max_length=13)

    class Meta:
        managed = False
        db_table = 'wp_wfls_2fa_secrets'


class WpWflsRoleCounts(models.Model):
    serialized_roles = models.CharField(primary_key=True, max_length=255)  # The composite primary key (serialized_roles, two_factor_inactive) found, that is not supported. The first column is selected.
    two_factor_inactive = models.IntegerField()
    user_count = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wfls_role_counts'
        unique_together = (('serialized_roles', 'two_factor_inactive'),)


class WpWflsSettings(models.Model):
    name = models.CharField(primary_key=True, max_length=191)
    value = models.TextField(blank=True, null=True)
    autoload = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'wp_wfls_settings'


class WpWpfmBackup(models.Model):
    backup_name = models.TextField(blank=True, null=True)
    backup_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_wpfm_backup'


class WpWpfrontUreOptions(models.Model):
    id = models.BigAutoField(unique=True)
    option_name = models.CharField(max_length=250, blank=True, null=True)
    option_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_wpfront_ure_options'


class WpWpilReportLinks(models.Model):
    link_id = models.BigAutoField(primary_key=True)
    post_id = models.PositiveBigIntegerField()
    clean_url = models.TextField(blank=True, null=True)
    raw_url = models.TextField(blank=True, null=True)
    host = models.TextField(blank=True, null=True)
    anchor = models.TextField(blank=True, null=True)
    internal = models.IntegerField(blank=True, null=True)
    has_links = models.IntegerField()
    post_type = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    broken_link_scanned = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_wpil_report_links'


class WpWplnstScans(models.Model):
    scan_id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    ready = models.IntegerField()
    hash = models.CharField(unique=True, max_length=32)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    modified_by = models.PositiveBigIntegerField()
    started_at = models.DateTimeField()
    enqueued_at = models.DateTimeField()
    stopped_at = models.DateTimeField()
    continued_at = models.DateTimeField()
    finished_at = models.DateTimeField()
    config = models.TextField()
    summary = models.TextField()
    trace = models.TextField()
    threads = models.TextField()
    max_threads = models.PositiveIntegerField()
    connect_timeout = models.PositiveIntegerField()
    request_timeout = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wplnst_scans'


class WpWplnstScansObjects(models.Model):
    scan_id = models.PositiveBigIntegerField(primary_key=True)  # The composite primary key (scan_id, object_id, object_type) found, that is not supported. The first column is selected.
    object_id = models.PositiveBigIntegerField()
    object_type = models.CharField(max_length=50)
    object_date_gmt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_wplnst_scans_objects'
        unique_together = (('scan_id', 'object_id', 'object_type'),)


class WpWplnstUrls(models.Model):
    url_id = models.BigAutoField(primary_key=True)
    url = models.TextField(db_collation='utf8mb3_bin')
    hash = models.CharField(unique=True, max_length=64)
    scheme = models.CharField(max_length=20)
    host = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    scope = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    last_scan_id = models.PositiveBigIntegerField()
    last_status_level = models.CharField(max_length=1)
    last_status_code = models.CharField(max_length=3)
    last_curl_errno = models.PositiveIntegerField()
    last_request_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'wp_wplnst_urls'


class WpWplnstUrlsLocations(models.Model):
    loc_id = models.BigAutoField(primary_key=True)
    url_id = models.PositiveBigIntegerField()
    scan_id = models.PositiveBigIntegerField()
    link_type = models.CharField(max_length=25)
    object_id = models.PositiveBigIntegerField()
    object_type = models.CharField(max_length=50)
    object_post_type = models.CharField(max_length=20)
    object_field = models.CharField(max_length=100)
    object_date_gmt = models.DateTimeField()
    detected_at = models.DateTimeField()
    chunk = models.TextField()
    anchor = models.TextField()
    raw_url = models.TextField()
    fragment = models.TextField()
    spaced = models.IntegerField()
    malformed = models.IntegerField()
    absolute = models.IntegerField()
    protorel = models.IntegerField()
    relative = models.IntegerField()
    nofollow = models.IntegerField()
    ignored = models.IntegerField()
    unlinked = models.IntegerField()
    modified = models.IntegerField()
    anchored = models.IntegerField()
    attributed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wplnst_urls_locations'


class WpWplnstUrlsLocationsAtt(models.Model):
    att_id = models.BigAutoField(primary_key=True)
    loc_id = models.PositiveBigIntegerField()
    scan_id = models.PositiveBigIntegerField()
    attribute = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wp_wplnst_urls_locations_att'


class WpWplnstUrlsStatus(models.Model):
    url_id = models.PositiveBigIntegerField(primary_key=True)  # The composite primary key (url_id, scan_id) found, that is not supported. The first column is selected.
    scan_id = models.PositiveBigIntegerField()
    status_level = models.CharField(max_length=1)
    status_code = models.CharField(max_length=3)
    curl_errno = models.PositiveIntegerField()
    redirect_url = models.TextField()
    redirect_steps = models.TextField()
    redirect_url_id = models.PositiveBigIntegerField()
    redirect_url_status = models.CharField(max_length=3)
    redirect_curl_errno = models.PositiveIntegerField()
    headers = models.TextField()
    headers_request = models.TextField()
    body = models.TextField()
    phase = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    started_at = models.DateTimeField()
    request_at = models.DateTimeField()
    total_objects = models.PositiveIntegerField()
    total_posts = models.PositiveIntegerField()
    total_comments = models.PositiveIntegerField()
    total_blogroll = models.PositiveIntegerField()
    total_time = models.DecimalField(max_digits=3, decimal_places=3)
    total_bytes = models.PositiveBigIntegerField()
    requests = models.PositiveIntegerField()
    rechecked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'wp_wplnst_urls_status'
        unique_together = (('url_id', 'scan_id'),)


class WpWpmcleaner(models.Model):
    id = models.BigAutoField(unique=True)
    time = models.DateTimeField()
    type = models.IntegerField()
    postid = models.BigIntegerField(db_column='postId', blank=True, null=True)  # Field name made lowercase.
    path = models.TextField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    ignored = models.IntegerField()
    deleted = models.IntegerField()
    issue = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_wpmcleaner'


class WpYoastIndexable(models.Model):
    permalink = models.TextField(blank=True, null=True)
    permalink_hash = models.CharField(max_length=40, blank=True, null=True)
    object_id = models.BigIntegerField(blank=True, null=True)
    object_type = models.CharField(max_length=32)
    object_sub_type = models.CharField(max_length=32, blank=True, null=True)
    author_id = models.BigIntegerField(blank=True, null=True)
    post_parent = models.BigIntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    breadcrumb_title = models.TextField(blank=True, null=True)
    post_status = models.CharField(max_length=20, blank=True, null=True)
    is_public = models.IntegerField(blank=True, null=True)
    is_protected = models.IntegerField(blank=True, null=True)
    has_public_posts = models.IntegerField(blank=True, null=True)
    number_of_pages = models.PositiveIntegerField(blank=True, null=True)
    canonical = models.TextField(blank=True, null=True)
    primary_focus_keyword = models.CharField(max_length=191, blank=True, null=True)
    primary_focus_keyword_score = models.IntegerField(blank=True, null=True)
    readability_score = models.IntegerField(blank=True, null=True)
    is_cornerstone = models.IntegerField(blank=True, null=True)
    is_robots_noindex = models.IntegerField(blank=True, null=True)
    is_robots_nofollow = models.IntegerField(blank=True, null=True)
    is_robots_noarchive = models.IntegerField(blank=True, null=True)
    is_robots_noimageindex = models.IntegerField(blank=True, null=True)
    is_robots_nosnippet = models.IntegerField(blank=True, null=True)
    twitter_title = models.TextField(blank=True, null=True)
    twitter_image = models.TextField(blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)
    twitter_image_id = models.CharField(max_length=191, blank=True, null=True)
    twitter_image_source = models.TextField(blank=True, null=True)
    open_graph_title = models.TextField(blank=True, null=True)
    open_graph_description = models.TextField(blank=True, null=True)
    open_graph_image = models.TextField(blank=True, null=True)
    open_graph_image_id = models.CharField(max_length=191, blank=True, null=True)
    open_graph_image_source = models.TextField(blank=True, null=True)
    open_graph_image_meta = models.TextField(blank=True, null=True)
    link_count = models.IntegerField(blank=True, null=True)
    incoming_link_count = models.IntegerField(blank=True, null=True)
    prominent_words_version = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    blog_id = models.BigIntegerField()
    language = models.CharField(max_length=32, blank=True, null=True)
    region = models.CharField(max_length=32, blank=True, null=True)
    schema_page_type = models.CharField(max_length=64, blank=True, null=True)
    schema_article_type = models.CharField(max_length=64, blank=True, null=True)
    has_ancestors = models.IntegerField(blank=True, null=True)
    estimated_reading_time_minutes = models.IntegerField(blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    object_last_modified = models.DateTimeField(blank=True, null=True)
    object_published_at = models.DateTimeField(blank=True, null=True)
    inclusive_language_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_yoast_indexable'


class WpYoastIndexableHierarchy(models.Model):
    indexable_id = models.PositiveIntegerField(primary_key=True)  # The composite primary key (indexable_id, ancestor_id) found, that is not supported. The first column is selected.
    ancestor_id = models.PositiveIntegerField()
    depth = models.PositiveIntegerField(blank=True, null=True)
    blog_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_yoast_indexable_hierarchy'
        unique_together = (('indexable_id', 'ancestor_id'),)


class WpYoastMigrations(models.Model):
    version = models.CharField(unique=True, max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_yoast_migrations'


class WpYoastPrimaryTerm(models.Model):
    post_id = models.BigIntegerField(blank=True, null=True)
    term_id = models.BigIntegerField(blank=True, null=True)
    taxonomy = models.CharField(max_length=32)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    blog_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'wp_yoast_primary_term'


class WpYoastProminentWords(models.Model):
    stem = models.CharField(max_length=191, blank=True, null=True)
    indexable_id = models.PositiveIntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_yoast_prominent_words'


class WpYoastSeoLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.CharField(max_length=255)
    post_id = models.PositiveBigIntegerField()
    target_post_id = models.PositiveBigIntegerField()
    type = models.CharField(max_length=8)
    indexable_id = models.PositiveIntegerField(blank=True, null=True)
    target_indexable_id = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    size = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(max_length=32, blank=True, null=True)
    region = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_yoast_seo_links'


class WpYoastSeoMeta(models.Model):
    object_id = models.PositiveBigIntegerField(unique=True)
    internal_link_count = models.PositiveIntegerField(blank=True, null=True)
    incoming_link_count = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wp_yoast_seo_meta'
