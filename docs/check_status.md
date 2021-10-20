Mojang have multiple APIs, you can check their status by calling the method [`status`][mojang.account.base.status]:

!!! Warning
    Since the begin of October 2021, Mojang closed down the status page ([Issue WEB-2303](https://bugs.mojang.com/browse/WEB-2303?focusedCommentId=1086543&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-1086543)). The [`status`][mojang.account.base.status] function now returns always the same response with an unknown status for each service.

::: mojang.account.base
    handler: python
    rendering:
        show_source: false
        show_root_toc_entry: false
    selection:
        members:
            - status
