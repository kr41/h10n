..  _the_problem:

The Problem or "Why do we need another i18n & l10n solution?"
=============================================================

Imagine, that you develop user interface of the content management
system, which is to be translated into some natural languages.
The CMS contains tens of object types.  Admin can perform tens of actions
with each object.  And each action is represented by several messages.
For example, object removal is accompanied by following ones:

*   Please, choose an ``{object.type}`` for removal.
*   Are you sure you want to delete this ``{object.type}``?
*   The ``{object.type}`` has been successfully deleted.

Traditional solution is to create separate translation string for each pair of
a message and an object type.  So, if you have 10 object types and 10 messages,
you need to create 100 translation strings for each language.  It obviously
makes you to perform tons of stupid copy-paste work.

Another way is to create two translation catalogs: first one should contain
message templates, second one -- object type names.  So, translation of any pair
of a message and an object is performed in three steps:

1.  Get message template;
2.  Get object type name;
3.  Put object type name into message template.

Very simple, no copy-paste, but doesn't work.  First of all you need to handle
special cases of natural languages.  For example, if you have "article" and
"comment" object types, the first message from the example above should be:

*   Please, choose **an** article for removal.
*   Please, choose **a** comment for removal.

As you can see, you also need to provide appropriate form of indefinite article.
Take notice, there is problem in English only.  If you try to translate these
messages in Russian, you will need to resolve another one: how to inflect
nouns by cases and associated verbs and prepositions according to noun's gender.

The best way to resolve these problems is to be able to write code and to store
meta data in translation string directly.  Existent solutions don't provide
these feature.  So, we need another one...
