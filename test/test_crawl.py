import unittest

from yuanpei_daoshi.crawl import _DaoshiHTMLParser


class TestDaoShiHTMLParser(unittest.TestCase):

    def test_name_and_gender(self):
        parser = _DaoshiHTMLParser()
        parser.feed('''
            <td style="width:80.65pt; padding-left:11.25pt; vertical-align:middle">
                        <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">姓名</span></p>
                                    </td>
                                                <td style="width:137.6pt; padding-left:11.25pt; vertical-align:middle">
                                                            <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">名字</span></p>
                                                                        </td>
                                                                                    <td style="width:73.8pt; padding-left:11.25pt; vertical-align:middle">
                                                                                                <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">性别</span></p>
                                                                                                            </td>
                                                                                                                        <td style="width:144.5pt; padding-left:11.25pt; vertical-align:middle">
                                                                                                                                    <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">男</span></p>
                                                                                                                                                </td>
''')
        assert parser.data == {'姓名': '名字', '性别': '男'}, f"got: {parser.data}"

    def test_graduation_school(self):
        parser = _DaoshiHTMLParser()
        parser.feed('''
            <td style="width:80.65pt; padding-left:11.25pt; vertical-align:middle">
                        <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">教育经历</span></p>
                                    </td>
                                                <td colspan="3" style="width:378.4pt; padding-left:11.25pt; vertical-align:middle">
                                                            <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">1995</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">年</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">北京大学理学 博士</span></p>

                                                                        <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">1992</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">年</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">北京大学理学 硕士</span></p>

                                                                                    <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">1989</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">年</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">吉林</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">大学理学</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> 学士</span></p>
                                                                                                </td>
''')
        assert parser.data == {'教育经历': ['1995年 北京大学理学 博士', '1992年 北京大学理学 硕士', '1989年 吉林大学理学 学士']}, f"got: {parser.data}"

    def test_achievements(self):
        parser = _DaoshiHTMLParser()
        parser.feed('''
<td style="width:80.65pt; padding-left:11.25pt; vertical-align:middle">
            <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">推荐书目</span></p>

                        <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">（1</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">-5</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">本）</span></p>
                                    </td>
                                                <td colspan="3" style="width:378.4pt; padding-left:11.25pt; vertical-align:middle">
                                                            <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">鲍林，《化学键的本质》</span></p>

                                                                        <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">詹</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">姆斯</span><span style="font-family:Symbol; font-size:9pt; letter-spacing:0.75pt"></span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">格雷克，《费曼传》</span></p>

                                                                                    <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">丹尼尔</span><span style="font-family:Symbol; font-size:9pt; letter-spacing:0.75pt"></span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">卡尼</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">曼</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">，《思考，快与慢》</span></p>

                                                                                                <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">卡尔</span><span style="font-family:Symbol; font-size:9pt; letter-spacing:0.75pt"></span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">萨</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">根，《魔鬼出没的世界》</span></p>

                                                                                                            <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">马尔科姆</span><span style="font-family:Symbol; font-size:9pt; letter-spacing:0.75pt"></span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">格拉德维尔，《异类》</span></p>
                                                                                                                        </td>
''')
        assert parser.data == {'推荐书目 （1 -5 本）': ['鲍林，《化学键的本质》', '詹姆斯\uf0d7格雷克，《费曼传》', '丹尼尔\uf0d7卡尼曼，《思考，快与慢》', '卡尔\uf0d7萨根，《魔鬼出没的世界》', '马尔科姆\uf0d7格拉德维尔，《异类》']}

    def test_single_td(self):
        parser = _DaoshiHTMLParser()
        parser.feed('''
<tr style="height:19.5pt">
            <td style="width:80.65pt; padding-left:11.25pt; vertical-align:middle">
                        <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">备注</span></p>
                                    </td>
                                            </tr>
                                                    <tr style="height:19.5pt">
                                                                <td style="width:80.65pt; padding-left:11.25pt; vertical-align:middle">
                                                                            <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">教育经历</span></p>
                                                                                        </td>
                                                                                                    <td colspan="3" style="width:378.4pt; padding-left:11.25pt; vertical-align:middle">
                                                                                                                <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">2002</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">年</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">美国斯坦福大学</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">经济学博士</span></p>

                                                                                                                            <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">1991</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">年</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">北京大学</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">经济学</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">院</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">经济学硕士</span></p>

                                                                                                                                        <p style="margin-top:0pt; margin-bottom:0pt; line-height:19.5pt"><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">1988</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">年</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">北京大学</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">经济学院 国际</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">经济学</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">系</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt"> </span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">经济</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">学</span><span style="font-family:微软雅黑; font-size:9pt; letter-spacing:0.75pt">学士</span></p>
                                                                                                                                                    </td>
                                                                                                                                                            </tr>
''')
        assert parser.data == {'备注': '', '教育经历': ['2002年 美国斯坦福大学 经济学博士', '1991年 北京大学 经济学院 经济学硕士', '1988年 北京大学 经济学院 国际经济学系 经济学学士']}


if __name__ == '__main__':
    unittest.main()

