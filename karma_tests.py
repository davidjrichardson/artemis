import unittest

from karma_parser import parse_message, create_transactions, RawKarma, KarmaTransaction


class TestKarmaProcessor(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(create_transactions('', []), None)

    def test_simple_positive(self):
        self.assertEqual(create_transactions('Baz', [RawKarma(name='Foobar', op='++', reason=None)]), [
            KarmaTransaction(name='Foobar', self_karma=False, net_karma=1, reasons=[])
        ])

    def test_simple_negative(self):
        self.assertEqual(create_transactions('Baz', [RawKarma(name='Foobar', op='--', reason=None)]), [
            KarmaTransaction(name='Foobar', self_karma=False, net_karma=-1, reasons=[])
        ])

    def test_simple_neutral(self):
        self.assertEqual(create_transactions('Baz', [RawKarma(name='Foobar', op='+-', reason=None)]), [
            KarmaTransaction(name='Foobar', self_karma=False, net_karma=0, reasons=[])
        ])

    def test_self_karma_single(self):
        self.assertEqual(create_transactions('Baz', [RawKarma(name='Baz', op='++', reason=None)]), [
            KarmaTransaction(name='Baz', self_karma=True, net_karma=0, reasons=[])
        ])

    def test_self_karma_multiple(self):
        self.assertEqual(create_transactions('Baz', [
            RawKarma(name='Baz', op='++', reason=None),
            RawKarma(name='Baz', op='++', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=True, net_karma=0, reasons=[])
                         ])

    def test_self_karma_single_with_others(self):
        self.assertEqual(create_transactions('Baz', [
            RawKarma(name='Baz', op='++', reason=None),
            RawKarma(name='Foobar', op='++', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=True, net_karma=0, reasons=[]),
                             KarmaTransaction(name='Foobar', self_karma=False, net_karma=1, reasons=[])
                         ])

    def test_karma_double_positive(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='++', reason=None),
            RawKarma(name='Baz', op='++', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=1, reasons=[])
                         ])

    def test_karma_double_negative(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='--', reason=None),
            RawKarma(name='Baz', op='--', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=-1, reasons=[])
                         ])

    def test_karma_double_neutral(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='+-', reason=None),
            RawKarma(name='Baz', op='-+', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=0, reasons=[])
                         ])

    def test_karma_positive_neutral(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='++', reason=None),
            RawKarma(name='Baz', op='+-', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=1, reasons=[])
                         ])

    def test_karma_negative_neutral(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='--', reason=None),
            RawKarma(name='Baz', op='+-', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=-1, reasons=[])
                         ])

    def test_karma_negative_positive(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='--', reason=None),
            RawKarma(name='Baz', op='++', reason=None)
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=0, reasons=[])
                         ])

    def test_simple_positive_reason(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='++', reason='Foobar is baz')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=1, reasons=['Foobar is baz'])
                         ])

    def test_simple_negative_reason(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='--', reason='Foobar is baz')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=-1, reasons=['Foobar is baz'])
                         ])

    def test_simple_neutral_reason(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='+-', reason='Foobar is baz')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=0,
                                              reasons=['Foobar is baz'])
                         ])

    def test_self_karma_single_reason(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Bar', op='++', reason='Is awesome')
        ]), [
                             KarmaTransaction(name='Bar', self_karma=True, net_karma=0, reasons=[])
                         ])

    def test_self_karma_multiple_reason(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Bar', op='++', reason='Is awesome'),
            RawKarma(name='Bar', op='++', reason='Is awesome')
        ]), [
                             KarmaTransaction(name='Bar', self_karma=True, net_karma=0, reasons=[])
                         ])

    def test_self_karma_single_with_others_and_reasons(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Bar', op='++', reason='Is awesome'),
            RawKarma(name='Foo', op='++', reason='Is awesome too'),
        ]), [
                             KarmaTransaction(name='Bar', self_karma=True, net_karma=0, reasons=[]),
                             KarmaTransaction(name='Foo', self_karma=False, net_karma=1, reasons=['Is awesome too'])
                         ])

    def test_karma_double_positive_reasons(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='++', reason='Foobar baz 1'),
            RawKarma(name='Baz', op='++', reason='Foobar baz 2')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=1,
                                              reasons=['Foobar baz 1', 'Foobar baz 2'])
                         ])

    def test_karma_double_negative_reasons(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='--', reason='Foobar baz 1'),
            RawKarma(name='Baz', op='--', reason='Foobar baz 2')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=-1,
                                              reasons=['Foobar baz 1', 'Foobar baz 2'])
                         ])

    def test_karma_double_neutral_reasons(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='-+', reason='Foobar baz 1'),
            RawKarma(name='Baz', op='+-', reason='Foobar baz 2')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=0,
                                              reasons=['Foobar baz 1', 'Foobar baz 2'])
                         ])

    def test_karma_positive_neutral_reasons(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='++', reason='Foobar baz 1'),
            RawKarma(name='Baz', op='+-', reason='Foobar baz 2')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=1,
                                              reasons=['Foobar baz 1', 'Foobar baz 2'])
                         ])

    def test_karma_negative_neutral_reasons(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='--', reason='Foobar baz 1'),
            RawKarma(name='Baz', op='+-', reason='Foobar baz 2')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=-1,
                                              reasons=['Foobar baz 1', 'Foobar baz 2'])
                         ])

    def test_karma_positive_negative_reasons(self):
        self.assertEqual(create_transactions('Bar', [
            RawKarma(name='Baz', op='++', reason='Foobar baz 1'),
            RawKarma(name='Baz', op='--', reason='Foobar baz 2')
        ]), [
                             KarmaTransaction(name='Baz', self_karma=False, net_karma=0,
                                              reasons=['Foobar baz 1', 'Foobar baz 2'])
                         ])


class TestKarmaParser(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(parse_message(''), None)

    def test_empty_with_code_block(self):
        self.assertEqual(parse_message('```FoobarBaz```'), None)

    def test_simple_positive(self):
        self.assertEqual(parse_message('Foobar++'), [RawKarma(name='Foobar', op='++', reason=None)])

    def test_simple_negative(self):
        self.assertEqual(parse_message('Foobar--'), [RawKarma(name='Foobar', op='--', reason=None)])

    def test_simple_neutral_pm(self):
        self.assertEqual(parse_message('Foobar+-'), [RawKarma(name='Foobar', op='+-', reason=None)])

    def test_simple_neutral_mp(self):
        self.assertEqual(parse_message('Foobar-+'), [RawKarma(name='Foobar', op='-+', reason=None)])

    def test_quoted_positive(self):
        self.assertEqual(parse_message('"Foobar"++'), [RawKarma(name='Foobar', op='++', reason=None)])

    def test_quoted_negative(self):
        self.assertEqual(parse_message('"Foobar"--'), [RawKarma(name='Foobar', op='--', reason=None)])

    def test_quoted_neutral_pm(self):
        self.assertEqual(parse_message('"Foobar"+-'), [RawKarma(name='Foobar', op='+-', reason=None)])

    def test_quoted_neutral_mp(self):
        self.assertEqual(parse_message('"Foobar"-+'), [RawKarma(name='Foobar', op='-+', reason=None)])

    def test_simple_positive_with_text_after(self):
        self.assertEqual(parse_message('Foobar++ since it\'s pretty cool'),
                         [RawKarma(name='Foobar', op='++', reason=None)])

    def test_simple_positive_with_parenthesis_after(self):
        self.assertEqual(parse_message('Foobar++ (hella cool)'), [RawKarma(name='Foobar', op='++', reason=None)])

    def test_simple_positive_with_reason(self):
        self.assertEqual(parse_message('Foobar++ because baz'), [RawKarma(name='Foobar', op='++', reason='baz')])

    def test_simple_negative_with_reason(self):
        self.assertEqual(parse_message('Foobar-- because baz'), [RawKarma(name='Foobar', op='--', reason='baz')])

    def test_simple_neutral_pm_with_reason(self):
        self.assertEqual(parse_message('Foobar+- because baz'), [RawKarma(name='Foobar', op='+-', reason='baz')])

    def test_simple_neutral_mp_with_reason(self):
        self.assertEqual(parse_message('Foobar-+ because baz'), [RawKarma(name='Foobar', op='-+', reason='baz')])

    def test_quoted_positive_with_reason(self):
        self.assertEqual(parse_message('"Foobar"++ because baz'), [RawKarma(name='Foobar', op='++', reason='baz')])

    def test_quoted_negative_with_reason(self):
        self.assertEqual(parse_message('"Foobar"-- because baz'), [RawKarma(name='Foobar', op='--', reason='baz')])

    def test_quoted_neutral_pm_with_reason(self):
        self.assertEqual(parse_message('"Foobar"+- because baz'), [RawKarma(name='Foobar', op='+-', reason='baz')])

    def test_quoted_neutral_mp_with_reason(self):
        self.assertEqual(parse_message('"Foobar"-+ because baz'), [RawKarma(name='Foobar', op='-+', reason='baz')])

    def test_simple_multiple_karma(self):
        self.assertEqual(parse_message('Foobar++, Baz-- Blat+-'), [
            RawKarma(name='Foobar', op='++', reason=None),
            RawKarma(name='Baz', op='--', reason=None),
            RawKarma(name='Blat', op='+-', reason=None)
        ])

    def test_simple_multiple_karma_with_some_reasons_and_quotes(self):
        self.assertEqual(parse_message('Foobar++ because baz blat, "Hello world"--'), [
            RawKarma(name='Foobar', op='++', reason='baz blat'),
            RawKarma(name='Hello world', op='--', reason=None)
        ])

    def test_karma_op_no_token(self):
        self.assertEqual(parse_message('++'), None)

    def test_simple_invalid(self):
        self.assertEqual(parse_message('Foo+'), None)

    def test_simple_not_start_of_sentence(self):
        self.assertEqual(parse_message('Hello, world! Foo++'), [RawKarma(name='Foo', op='++', reason=None)])

    def test_simple_invalid_with_reason(self):
        self.assertEqual(parse_message('Foo+ because bar'), None)

    def test_code_block_with_internal_reason(self):
        self.assertEqual(parse_message('```Foobar baz because foo```'), None)

    def test_code_block_with_karma_op_after(self):
        self.assertEqual(parse_message('```Foobar baz```++'), None)

    def test_code_block_external_reason(self):
        self.assertEqual(parse_message('```Foobar baz``` because foo'), None)

    def test_code_block_with_karma_op_after_and_external_reason(self):
        self.assertEqual(parse_message('```Foobar baz```++ because foo'), None)


if __name__ == '__main__':
    unittest.main()
