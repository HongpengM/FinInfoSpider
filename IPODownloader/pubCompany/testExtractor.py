import tableExtractor
html0 = '''<table><tr><td><a href='http://www'>1</a></td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>'''
html1 = '''<table class="table_grey_border ms-rteTable-BlueTable_CHI" style="800px" summary="">
                      <thead>
                       <tr class="tr_header ms-rteTableHeaderRow-BlueTable_ENG">
                        <th class="verd_black12 ms-rteTableHeaderEvenCol-BlueTable_ENG" style="width:130px;">
                         <p align="left">
                          <strong>
                           最新發佈日期
                          </strong>
                          <img border="0" height="9" src="/image/down_blue.gif" width="15"/>
                          /
                          <a href="SEHKAPPMainIndex_date_asc_c.htm" style="cursor:pointer;">
                           <img border="0" height="9" src="/image/up.gif" width="15"/>
                          </a>
                         </p>
                        </th>
                        <th class="verd_black12 ms-rteTableEvenCol-BlueTable_ENG" style="width:600px;">
                         <p align="left">
                          <strong>
                           申請人
                          </strong>
                          <a href="SEHKAPPMainIndex_name_desc_c.htm" style="cursor:pointer;">
                           <img border="0" height="9" src="/image/down.gif" width="15"/>
                          </a>
                          /
                          <a href="SEHKAPPMainIndex_name_asc_c.htm" style="cursor:pointer;">
                           <img border="0" height="9" src="/image/up.gif" width="15"/>
                          </a>
                         </p>
                        </th>
                       </tr>
                      </thead>
                      <tbody>
                       <tr class="tr_header ms-rteTableHeaderRow-BlueTable_CHI">
                        <td class="tr_subheader verd_black12 ms-rteTableEvenCol-BlueTable_CHI" colspan="2" height="1">
                         <p align="left">
                          <strong>
                           (A) 僅刊發申請版本的申請人
                          </strong>
                         </p>
                        </td>
                       </tr>
                       <tr class="tr_normal ms-rteTableOddRow-BlueTable_CHI">
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         2018-04-27
                        </td>
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         <a href="SEHK/2018/2018042601/SEHKWarningStatement-2018042601_c.htm" title="">
                          安樂工程集團有限公司
                         </a>
                        </td>
                       </tr>
                       <tr class="tr_normal ms-rteTableOddRow-BlueTable_CHI">
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         2018-01-03
                        </td>
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         <a href="SEHK/2018/2018010202/SEHKWarningStatement-2018010202_c.htm" title="">
                          麗柏集團（控股）有限公司
                         </a>
                        </td>
                       </tr>
                       <tr class="tr_normal ms-rteTableOddRow-BlueTable_CHI">
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         2017-12-28
                        </td>
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         <a href="SEHK/2017/2017122201/SEHKWarningStatement-2017122201_c.htm" title="">
                          华立大学集团有限公司
                         </a>
                        </td>
                       </tr>
                       <tr class="tr_normal ms-rteTableOddRow-BlueTable_CHI">
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         2017-12-28
                        </td>
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         <a href="SEHK/2017/2017122701/SEHKWarningStatement-2017122701_c.htm" title="">
                          金盾控股(實業)有限公司
                         </a>
                        </td>
                       </tr>
                       <tr class="tr_normal ms-rteTableOddRow-BlueTable_CHI">
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         2017-12-28
                        </td>
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         <a href="SEHK/2017/2017122801/SEHKWarningStatement-2017122801_c.htm" title="">
                          新綠色藥業科技發展（開曼）有限公司
                         </a>
                        </td>
                       </tr>
                       
                       <tr class="tr_header ms-rteTableHeaderRow-BlueTable_CHI">
                        <td class="tr_subheader verd_black12 ms-rteTableEvenCol-BlueTable_CHI" colspan="2" height="1">
                         <p align="left">
                          <strong>
                           (B) 已刊發申請版本及聆訊後資料集的申請人
                          </strong>
                         </p>
                        </td>
                       </tr>
                       
                       <tr class="tr_normal ms-rteTableOddRow-BlueTable_CHI">
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         2017-10-26
                        </td>
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         <a href="SEHK/2017/2017092605/SEHKWarningStatement-2017092605_c.htm" title="">
                          佑威國際控股有限公司
                         </a>
                        </td>
                       </tr>
                       <tr class="tr_normal ms-rteTableOddRow-BlueTable_CHI">
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         2017-09-29
                        </td>
                        <td class="pming_black12 ms-rteTableOddCol-BlueTable_CHI">
                         <a href="SEHK/2017/2017040301/SEHKWarningStatement-2017040301_c.htm" title="">
                          V3 Group Limited
                         </a>
                        </td>
                       </tr>
                      </tbody>
                     </table>'''
extractor = tableExtractor.Extractor(html1)
extractor.parse()
print(extractor.return_list())
extractor.write_to_csv()
