# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import jinja2
from django_jinja import library
from markupsafe import Markup

from lib.l10n_utils import fluent


@library.global_function
@jinja2.pass_context
def ftl(ctx, message_id, fallback=None, locale=None, **kwargs):
    """Return the translated string.

    :param ctx: the context from the template (automatically included)
    :param str message_id: the ID of the message
    :param str fallback: the ID of a message to use if message_id is not translated
    :param str locale: If set the string returned will be from the given locale instead of the current one
    :param kwargs: the other kwargs are passed to the translation as variables
    :return: the translated string marked as safe

    Usage example::

        <p>{{ ftl('greeting', name='The Dude') }}
    """
    if locale:
        return Markup(fluent.ftl(message_id, fallback, locale=locale, ftl_files=ctx["fluent_files"], **kwargs))

    l10n = ctx["fluent_l10n"]
    return Markup(fluent.translate(l10n, message_id, fallback, **kwargs))


@library.global_function
@jinja2.pass_context
def ftl_has_messages(ctx, *message_ids, require_all=True):
    """Return True if the current translation has all of the message IDs."""
    return fluent.ftl_has_messages(ctx["fluent_l10n"], *message_ids, require_all=require_all)


@library.global_function
def ftl_file_is_active(ftl_file):
    return fluent.ftl_file_is_active(ftl_file)
