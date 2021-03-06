# -*- coding: utf-8 -*-
#
# Copyright 2007-2011 Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""This module stores information and functionality that relates to plurals."""

import gettext
import locale
import os
import re
import six


languages = {
    'ach': (u'Acholi', 2, 'n > 1'),
    'af': (u'Afrikaans', 2, '(n != 1)'),
    'ak': (u'Akan', 2, 'n > 1'),
    'am': (u'Amharic', 2, 'n > 1'),
    'an': (u'Aragonese', 2, '(n != 1)'),
    'anp': (u'Angika', 2, '(n != 1)'),
    'ar': (u'Arabic', 6,
           'n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5'),
    'arn': (u'Mapudungun; Mapuche', 2, 'n > 1'),
    'as': (u'Assamese', 2, '(n != 1)'),
    'ast': (u'Asturian; Bable; Leonese; Asturleonese', 2, '(n != 1)'),
    'ay': (u'Aymará', 1, '0'),
    'az': (u'Azerbaijani', 2, '(n != 1)'),
    'be': (u'Belarusian', 3,
           'n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2'),
    'bg': (u'Bulgarian', 2, '(n != 1)'),
    'bn': (u'Bengali', 2, '(n != 1)'),
    'bn_IN': (u'Bengali (India)', 2, '(n != 1)'),
    'bo': (u'Tibetan', 1, '0'),
    'br': (u'Breton', 2, 'n > 1'),
    'brx': (u'Bodo', 2, '(n != 1)'),
    'bs': (u'Bosnian', 3,
           'n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2'),
    'ca': (u'Catalan; Valencian', 2, '(n != 1)'),
    'ca@valencia': (u'Catalan; Valencian (Valencia)', 2, '(n != 1)'),
    'cgg': (u'Chiga', 1, '0'),
    'cs': (u'Czech', 3, '(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2'),
    'csb': (u'Kashubian', 3,
            'n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2'),
    'cy': (u'Welsh', 2, '(n==2) ? 1 : 0'),
    'da': (u'Danish', 2, '(n != 1)'),
    'de': (u'German', 2, '(n != 1)'),
    'doi': (u'Dogri', 2, '(n != 1)'),
    'dz': (u'Dzongkha', 1, '0'),
    'el': (u'Greek, Modern (1453-)', 2, '(n != 1)'),
    'en': (u'English', 2, '(n != 1)'),
    'en_GB': (u'English (United Kingdom)', 2, '(n != 1)'),
    'en_ZA': (u'English (South Africa)', 2, '(n != 1)'),
    'eo': (u'Esperanto', 2, '(n != 1)'),
    'es': (u'Spanish; Castilian', 2, '(n != 1)'),
    'es_AR': (u'Argentinean Spanish', 2, '(n != 1)'),
    'et': (u'Estonian', 2, '(n != 1)'),
    'eu': (u'Basque', 2, '(n != 1)'),
    'fa': (u'Persian', 1, '0'),
    'ff': (u'Fulah', 2, '(n != 1)'),
    'fi': (u'Finnish', 2, '(n != 1)'),
    'fil': (u'Filipino; Pilipino', 2, '(n > 1)'),
    'fo': (u'Faroese', 2, '(n != 1)'),
    'fr': (u'French', 2, '(n > 1)'),
    'fur': (u'Friulian', 2, '(n != 1)'),
    'fy': (u'Frisian', 2, '(n != 1)'),
    'ga': (u'Irish', 5, 'n==1 ? 0 : n==2 ? 1 : (n>2 && n<7) ? 2 :(n>6 && n<11) ? 3 : 4'),
    'gd': (u'Gaelic; Scottish Gaelic', 4, '(n==1 || n==11) ? 0 : (n==2 || n==12) ? 1 : (n > 2 && n < 20) ? 2 : 3'),
    'gl': (u'Galician', 2, '(n != 1)'),
    'gu': (u'Gujarati', 2, '(n != 1)'),
    'gun': (u'Gun', 2, '(n > 1)'),
    'ha': (u'Hausa', 2, '(n != 1)'),
    'he': (u'Hebrew', 2, '(n != 1)'),
    'hi': (u'Hindi', 2, '(n != 1)'),
    'hne': (u'Chhattisgarhi', 2, '(n != 1)'),
    'hr': (u'Croatian', 3, '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'),
    'ht': (u'Haitian; Haitian Creole', 2, '(n != 1)'),
    'hu': (u'Hungarian', 2, '(n != 1)'),
    'hy': (u'Armenian', 1, '0'),
    'ia': (u"Interlingua (International Auxiliary Language Association)", 2, '(n != 1)'),
    'id': (u'Indonesian', 1, '0'),
    'is': (u'Icelandic', 2, '(n != 1)'),
    'it': (u'Italian', 2, '(n != 1)'),
    'ja': (u'Japanese', 1, '0'),
    'jbo': (u'Lojban', 1, '0'),
    'jv': (u'Javanese', 2, '(n != 1)'),
    'ka': (u'Georgian', 1, '0'),
    'kk': (u'Kazakh', 1, '0'),
    'kl': (u'Greenlandic', 2, '(n != 1)'),
    'km': (u'Central Khmer', 1, '0'),
    'kn': (u'Kannada', 2, '(n != 1)'),
    'ko': (u'Korean', 1, '0'),
    'ku': (u'Kurdish', 2, '(n != 1)'),
    'kw': (u'Cornish', 4, '(n==1) ? 0 : (n==2) ? 1 : (n == 3) ? 2 : 3'),
    'ky': (u'Kirghiz; Kyrgyz', 1, '0'),
    'lb': (u'Luxembourgish; Letzeburgesch', 2, '(n != 1)'),
    'ln': (u'Lingala', 2, '(n > 1)'),
    'lo': (u'Lao', 1, '0'),
    'lt': (u'Lithuanian', 3, '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && (n%100<10 || n%100>=20) ? 1 : 2)'),
    'lv': (u'Latvian', 3, '(n%10==1 && n%100!=11 ? 0 : n != 0 ? 1 : 2)'),
    'mai': (u'Maithili', 2, '(n != 1)'),
    'mfe': (u'Morisyen', 2, '(n > 1)'),
    'mg': (u'Malagasy', 2, '(n > 1)'),
    'mi': (u'Maori', 2, '(n > 1)'),
    'mk': (u'Macedonian', 2, 'n==1 || n%10==1 ? 0 : 1'),
    'ml': (u'Malayalam', 2, '(n != 1)'),
    'mn': (u'Mongolian', 2, '(n != 1)'),
    'mni': (u'Manipuri', 2, '(n != 1)'),
    'mnk': (u'Mandinka', 3, '(n==0 ? 0 : n==1 ? 1 : 2)'),
    'mr': (u'Marathi', 2, '(n != 1)'),
    'ms': (u'Malay', 1, '0'),
    'mt': (u'Maltese', 4,
           '(n==1 ? 0 : n==0 || ( n%100>1 && n%100<11) ? 1 : (n%100>10 && n%100<20 ) ? 2 : 3)'),
    'my': (u'Burmese', 1, '0'),
    'nah': (u'Nahuatl languages', 2, '(n != 1)'),
    'nap': (u'Neapolitan', 2, '(n != 1)'),
    'nb': (u'Bokmål, Norwegian; Norwegian Bokmål', 2, '(n != 1)'),
    'ne': (u'Nepali', 2, '(n != 1)'),
    'nl': (u'Dutch; Flemish', 2, '(n != 1)'),
    'nn': (u'Norwegian Nynorsk; Nynorsk, Norwegian', 2, '(n != 1)'),
    'nqo': (u"N'Ko", 2, '(n > 1)'),
    'nso': (u'Pedi; Sepedi; Northern Sotho', 2, '(n != 1)'),
    'oc': (u'Occitan (post 1500)', 2, '(n > 1)'),
    'or': (u'Oriya', 2, '(n != 1)'),
    'pa': (u'Panjabi; Punjabi', 2, '(n != 1)'),
    'pap': (u'Papiamento', 2, '(n != 1)'),
    'pl': (u'Polish', 3,
           '(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'),
    'pms': (u'Piemontese', 2, '(n != 1)'),
    'ps': (u'Pushto; Pashto', 2, '(n != 1)'),
    'pt': (u'Portuguese', 2, '(n != 1)'),
    'pt_BR': (u'Portuguese (Brazil)', 2, '(n > 1)'),
    'rm': (u'Romansh', 2, '(n != 1)'),
    'ro': (u'Romanian', 3, '(n==1 ? 0 : (n==0 || (n%100 > 0 && n%100 < 20)) ? 1 : 2);'),
    'ru': (u'Russian', 3,
          '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'),
    'rw': (u'Kinyarwanda', 2, '(n != 1)'),
    'sah': (u'Yakut', 1, '0'),
    'sat': (u'Santali', 2, '(n != 1)'),
    'sco': (u'Scots', 2, '(n != 1)'),
    'sd': (u'Sindhi', 2, '(n != 1)'),
    'se': (u'Northern Sami', 2, '(n != 1)'),
    'si': (u'Sinhala; Sinhalese', 2, '(n != 1)'),
    'sk': (u'Slovak', 3, '(n==1) ? 0 : (n>=2 && n<=4) ? 1 : 2'),
    'sl': (u'Slovenian', 4, '(n%100==1 ? 1 : n%100==2 ? 2 : n%100==3 || n%100==4 ? 3 : 0)'),
    'so': (u'Somali', 2, '(n != 1)'),
    'son': (u'Songhai languages', 2, '(n != 1)'),
    'sq': (u'Albanian', 2, '(n != 1)'),
    'sr': (u'Serbian', 3,
           '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'),
    'st': (u'Sotho, Southern', 2, '(n != 1)'),
    'su': (u'Sundanese', 1, '0'),
    'sv': (u'Swedish', 2, '(n != 1)'),
    'sw': (u'Swahili', 2, '(n != 1)'),
    'ta': (u'Tamil', 2, '(n != 1)'),
    'te': (u'Telugu', 2, '(n != 1)'),
    'tg': (u'Tajik', 2, '(n != 1)'),
    'th': (u'Thai', 1, '0'),
    'ti': (u'Tigrinya', 2, '(n > 1)'),
    'tk': (u'Turkmen', 2, '(n != 1)'),
    'tr': (u'Turkish', 1, '0'),
    'tt': (u'Tatar', 1, '0'),
    'ug': (u'Uighur; Uyghur', 1, '0'),
    'uk': (u'Ukrainian', 3,
           '(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)'),
    'ur': (u'Urdu', 2, '(n != 1)'),
    'uz': (u'Uzbek', 2, '(n > 1)'),
    've': (u'Venda', 2, '(n != 1)'),
    'vi': (u'Vietnamese', 1, '0'),
    'wa': (u'Walloon', 2, '(n > 1)'),
    'wo': (u'Wolof', 2, '(n != 1)'),
    'yo': (u'Yoruba', 2, '(n != 1)'),
    # Chinese is difficult because the main divide is on script, not really
    # country. Simplified Chinese is used mostly in China, Singapore and Malaysia.
    # Traditional Chinese is used mostly in Hong Kong, Taiwan and Macau.
    'zh_CN': (u'Chinese (China)', 1, '0'),
    'zh_HK': (u'Chinese (Hong Kong)', 1, '0'),
    'zh_TW': (u'Chinese (Taiwan)', 1, '0'),
    'zu': (u'Zulu', 2, '(n != 1)'),
}
"""Dictionary of language data.
The language code is the dictionary key (which may contain country codes
and modifiers).  The value is a tuple: (Full name in English from iso-codes,
nplurals, plural equation).

Note that the English names should not be used in user facing places - it
should always be passed through the function returned from tr_lang(), or at
least passed through _fix_language_name()."""

_fixed_names = {
    u"Asturian; Bable; Leonese; Asturleonese": u"Asturian",
    u"Bokmål, Norwegian; Norwegian Bokmål": u"Norwegian Bokmål",
    u"Catalan; Valencian": u"Catalan",
    u"Central Khmer": u"Khmer",
    u"Chichewa; Chewa; Nyanja": u"Chewa; Nyanja",
    u"Divehi; Dhivehi; Maldivian": u"Divehi",
    u"Dutch; Flemish": u"Dutch",
    u"Filipino; Pilipino": u"Filipino",
    u"Gaelic; Scottish Gaelic": u"Scottish Gaelic",
    u"Greek, Modern (1453-)": u"Greek",
    u"Interlingua (International Auxiliary Language Association)": u"Interlingua",
    u"Kirghiz; Kyrgyz": u"Kirghiz",
    u"Klingon; tlhIngan-Hol": u"Klingon",
    u"Limburgan; Limburger; Limburgish": u"Limburgish",
    u"Low German; Low Saxon; German, Low; Saxon, Low": u"Low German",
    u"Luxembourgish; Letzeburgesch": u"Luxembourgish",
    u"Ndebele, South; South Ndebele": u"Southern Ndebele",
    u"Norwegian Nynorsk; Nynorsk, Norwegian": u"Norwegian Nynorsk",
    u"Occitan (post 1500)": u"Occitan",
    u"Panjabi; Punjabi": u"Punjabi",
    u"Pedi; Sepedi; Northern Sotho": u"Northern Sotho",
    u"Pushto; Pashto": u"Pashto",
    u"Sinhala; Sinhalese": u"Sinhala",
    u"Songhai languages": u"Songhay",
    u"Sotho, Southern": u"Sotho",
    u"Spanish; Castilian": u"Spanish",
    u"Uighur; Uyghur": u"Uyghur",
}


cldr_plural_categories = [
        'zero',
        'one',
        'two',
        'few',
        'many',
        'other',
]


def simplercode(code):
    """This attempts to simplify the given language code by ignoring country
    codes, for example.

    .. seealso::

       - http://www.rfc-editor.org/rfc/bcp/bcp47.txt
       - http://www.rfc-editor.org/rfc/rfc4646.txt
       - http://www.rfc-editor.org/rfc/rfc4647.txt
       - http://www.w3.org/International/articles/language-tags/
    """
    if not code:
        return code

    normalized = normalize_code(code)
    separator = normalized.rfind('-')
    if separator >= 0:
        return code[:separator]
    else:
        return ""


expansion_factors = {
        'af': 0.1,
        'ar': -0.09,
        'es': 0.21,
        'fr': 0.28,
        'it': 0.2,
}
"""Source to target string length expansion factors."""

iso639 = {}
"""ISO 639 language codes"""
iso3166 = {}
"""ISO 3166 country codes"""

langcode_re = re.compile("^[a-z]{2,3}([_-][A-Z]{2,3}|)(@[a-zA-Z0-9]+|)$")
langcode_ire = re.compile("^[a-z]{2,3}([_-][a-z]{2,3})?(@[a-z0-9]+)?$",
                          re.IGNORECASE)
variant_re = re.compile("^[_-][A-Z]{2,3}(@[a-zA-Z0-9]+|)$")


def languagematch(languagecode, otherlanguagecode):
    """matches a languagecode to another, ignoring regions in the second"""
    if languagecode is None:
        return langcode_re.match(otherlanguagecode)
    return languagecode == otherlanguagecode or \
           (otherlanguagecode.startswith(languagecode) and
            variant_re.match(otherlanguagecode[len(languagecode):]))

dialect_name_re = re.compile(r"(.+)\s\(([^)\d]{,25})\)$")
# The limit of 25 characters on the country name is so that "Interlingua (...)"
# (see above) is correctly interpreted.


def tr_lang(langcode=None):
    """Gives a function that can translate a language name, even in the
    form ``"language (country)"``, into the language with iso code langcode,
    or the system language if no language is specified."""
    langfunc = gettext_lang(langcode)
    countryfunc = gettext_country(langcode)

    def handlelanguage(name):
        match = dialect_name_re.match(name)
        if match:
            language, country = match.groups()
            return u"%s (%s)" % (_fix_language_name(langfunc(language)),
                                 countryfunc(country))
        else:
            return _fix_language_name(langfunc(name))

    return handlelanguage


def _fix_language_name(name):
    """Identify and replace some unsightly names present in iso-codes.

    If the name is present in _fixed_names we assume it is untranslated and
    we replace it with a more usable rendering.  If the remaining part is long
    and includes a semi-colon, we only take the text up to the semi-colon to
    keep things neat."""
    if name in _fixed_names:
        return _fixed_names[name]
    elif len(name) > 11:
        # These constants are somewhat arbitrary, but testing with the Japanese
        # translation of ISO codes suggests these as the upper bounds.
        split_point = name[5:].find(u';')
        if split_point >= 0:
            return name[:5+split_point]
    return name


def gettext_lang(langcode=None):
    """Returns a gettext function to translate language names into the given
    language, or the system language if no language is specified."""
    if not langcode in iso639:
        if not langcode:
            langcode = ""
            if os.name == "nt":
                # On Windows the default locale is not used for some reason
                t = gettext.translation('iso_639',
                                        languages=[locale.getdefaultlocale()[0]],
                                        fallback=True)
            else:
                t = gettext.translation('iso_639', fallback=True)
        else:
            t = gettext.translation('iso_639', languages=[langcode],
                                    fallback=True)
        iso639[langcode] = t.ugettext if six.PY2 else t.gettext
    return iso639[langcode]


def gettext_country(langcode=None):
    """Returns a gettext function to translate country names into the given
    language, or the system language if no language is specified."""
    if not langcode in iso3166:
        if not langcode:
            langcode = ""
            if os.name == "nt":
                # On Windows the default locale is not used for some reason
                t = gettext.translation('iso_3166',
                                        languages=[locale.getdefaultlocale()[0]],
                                        fallback=True)
            else:
                t = gettext.translation('iso_3166', fallback=True)
        else:
            t = gettext.translation('iso_3166', languages=[langcode],
                                    fallback=True)
        iso3166[langcode] = t.ugettext if six.PY2 else t.gettext
    return iso3166[langcode]


def normalize(string, normal_form="NFC"):
    """Return a unicode string in its normalized form

       :param string: The string to be normalized
       :param normal_form: NFC (default), NFD, NFKC, NFKD
       :return: Normalized string
    """
    if string is None:
        return None
    else:
        import unicodedata
        return unicodedata.normalize(normal_form, string)


def forceunicode(string):
    """Ensures that the string is in unicode.

       :param string: A text string
       :type string: Unicode, String
       :return: String converted to Unicode and normalized as needed.
       :rtype: Unicode
    """
    if string is None:
        return None
    from translate.storage.placeables import StringElem
    if isinstance(string, bytes):
        encoding = getattr(string, "encoding", "utf-8")
        string = string.decode(encoding)
    elif isinstance(string, StringElem):
        string = six.text_type(string)
    return string


def normalized_unicode(string):
    """Forces the string to unicode and does normalization."""
    return normalize(forceunicode(string))


def normalize_code(code):
    if not code:
        return code
    return code.replace("_", "-").replace("@", "-").lower()


__normalised_languages = set(normalize_code(key) for key in languages.keys())


def simplify_to_common(language_code, languages=languages):
    """Simplify language code to the most commonly used form for the
    language, stripping country information for languages that tend
    not to be localized differently for different countries"""
    simpler = simplercode(language_code)
    if simpler == "":
        return language_code

    if (normalize_code(language_code) in __normalised_languages):
        return language_code

    return simplify_to_common(simpler)


def get_language(code):
    code = code.replace("-", "_").replace("@", "_").lower()
    if "_" in code:
        # convert ab_cd → ab_CD
        code = "%s_%s" % (code.split("_")[0], code.split("_", 1)[1].upper())
    return languages.get(code, None)
