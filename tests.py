# coding: utf-8
import pytest
import string

from check_email_cython import check_email


@pytest.mark.parametrize("name, domain", [('good', 'ya.ru')])
@pytest.mark.parametrize("delimiter", ['$', '%', '', '#'])
def test_without_at_delimiter(name, domain, delimiter):
    email = delimiter.join([name, domain])
    assert check_email(email) == False


@pytest.mark.parametrize("name,result", [
    ('', False),
    ('a', True),
    ('128_' + 'a' * 124, True),
    ('129_' + 'a' * 125, False)])
@pytest.mark.parametrize("domain", ['ya.ru'])
def test_name_length(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("name", ['good'])
@pytest.mark.parametrize("domain,result", [
    ('ya.ru', True),
    ('', False),
    ('y', False),
    ('ya', False),
    ('yup', True),
    ('256_' + 'ya' * 126, True),
    ('257_' + 'y' * 253, False)
])
def test_domain_length(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("name", ['good'])
@pytest.mark.parametrize("domain,result", [
    ('two..dots', False),
    ('m.a.n.y.d.o.t.s', True),
    ('.starts.with.dot', False),
    ('ends.with.dot.', False),
])
def test_dots_in_domain(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("name", ['good'])
@pytest.mark.parametrize("domain,result", [
    ('with-dash.ru', True),
    ('double--dash', True),
    ('ends-', False),
    ('-starts', False),
    ('before-.dot', False),
    ('after.-dot' * 128, False),
])
def test_dashes_in_domain(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("name", [
    'UPPERCASE',
    'Starts_with_uppercase',
    'ends_with_uppercasE',
    'containS.uppErcaSe'])
@pytest.mark.parametrize("domain", ['ya.ru'])
def test_uppercase_name(name, domain):
    email = '@'.join([name, domain])
    assert check_email(email) == False


@pytest.mark.parametrize("name", ['good.email'])
@pytest.mark.parametrize("domain", ['YA.RU', 'Ya.ru', 'ya.rU', 'yA.Ru'])
def test_uppercase_domain(name, domain):
    email = '@'.join([name, domain])
    assert check_email(email) == False


@pytest.mark.parametrize("name,result", [
    ('.', True),
    ('one.dot', True),
    ('two..dots', False),
    ('"two..dots"', False),
    ('dots.are.separated', True)])
@pytest.mark.parametrize("domain", ['ya.ru'])
def test_dots_in_name(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("name,result", [
    ('""', True),
    ('"', False),
    ('quotes_after""', True),
    ('""quotes_before', True),
    ('quotes""between', True),
    ('"dots.in.quotes"', True),
    ('here""several""quotes""', True),
    ('odd"number"of"quotes', False),
    ('special"characters,"inside"quo:tes!"', True),
    ('special"characters":"outside"quotes!', False),
    ('special"characters"both"sides"!', False),
    ('special" characters # "are"predefined?"', False),
])
@pytest.mark.parametrize("domain", ['ya.ru'])
def test_names_with_quotes(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("name,result", [
    (string.ascii_lowercase, True),
    (string.digits, True),
    ('_.-"_.-!:,"', True)] + [(char, False) for char in '!@#$%^&*()+=\|?']
)
@pytest.mark.parametrize("domain", ['ya.ru'])
def test_nvalid_characters_in_name(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("name", ['good'])
@pytest.mark.parametrize("domain,result", [
    (string.ascii_lowercase, True),
    (string.digits, True),
    ('_.o-o', True)] + [(char * 3, False) for char in '!@#$%^&*()+=\|?:,']
)
def test_invalid_characters_in_domain(name, domain, result):
    email = '@'.join([name, domain])
    assert check_email(email) == result


@pytest.mark.parametrize("input_str", [0, ['god@ya.ru'], {}, object(), str])
def test_wrong_input(input_str):
    with pytest.raises(TypeError):
        check_email(input_str)


@pytest.mark.parametrize("name,name_result", [(u'good', True), (u'кириллица', False)])
@pytest.mark.parametrize("domain,domain_result", [(u'ya.ru', True), (u'секс.рф', False)])
def test_unicode(name, name_result, domain, domain_result):
    email = '@'.join([name, domain])
    assert check_email(email) == (name_result and domain_result)


@pytest.mark.timeout(1)
def test_time_attack():
    very_long_email = "%(string)s@%(string)s.ru" % {'string': 'long' * 100000}
    for _ in xrange(100000):
        check_email(very_long_email)
