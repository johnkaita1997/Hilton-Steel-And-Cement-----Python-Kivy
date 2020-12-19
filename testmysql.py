# import docx
# from PIL import Image, ImageOps
# from PIL import ImageFont
# from PIL import ImageDraw
# from docx import Document
# import re
# from docx import Document
# import os
# import argparse
# from PyPDF2 import PdfFileReader, PdfFileWriter
# from docx2pdf import convert
#
#
# # img = Image.open("a.jpg")
# # draw = ImageDraw.Draw(img)
# # # font = ImageFont.truetype(<font-file>, <font-size>)
# # font = ImageFont.truetype("arial.ttf", 16)
# # # draw.text((x, y),"Sample Text",(r,g,b))
# # draw.text((0, 0),"Sample Text",(255,255,255),font=font)
# # img.save('C:\\Users\\John\\Desktop\\See\\sample-out.jpg')
#
#
# # image1 = Image.new('RGBA', (200, 150), (0, 128, 0, 92))
# font = ImageFont.truetype(r'arial.ttf', 30)
# image = Image.open("a.jpg")
#
# #Draw text into a temporary blank image, rotate that, then paste that onto the original image
# text1 = 'TEST'
# width1, height1 = font.getsize(text1)
# draw1 = ImageDraw.Draw(image)
# draw1.text((0, 0), text=text1, font=font, fill=(255, 128, 0))
# image1 = Image.new('RGBA', (width1, height1), (0, 0, 128, 92))
# draw1 = ImageDraw.Draw(image1)
# draw1.text((0, 0), text=text1, font=font, fill=(0, 255, 128))
# image1 = image1.rotate(30, expand=1)
# image.paste(image1, (0, 460), image1)
#
# text2 = 'Love is blind'
# width2, height2 = font.getsize(text2)
# draw2 = ImageDraw.Draw(image)
# draw2.text((0, 0), text=text2, font=font, fill=(0, 255, 128))
# image2 = Image.new('RGBA', (width2, height2), (0, 0, 128, 92))
# draw2 = ImageDraw.Draw(image2)
# draw2.text((0, 0), text=text2, font=font, fill=(0, 255, 128))
# image2 = image2.rotate(30, expand=1)
# image.paste(image2, (0, 860), image2)
#
#
# text3 = 'Love is blind'
# width3, height3 = font.getsize(text3)
# draw3 = ImageDraw.Draw(image)
# draw3.text((0, 0), text=text2, font=font, fill=(0, 255, 128))
# image3 = Image.new('RGBA', (width3, height3), (0, 0, 128, 92))
# draw3 = ImageDraw.Draw(image3)
# draw3.text((0, 0), text=text3, font=font, fill=(0, 255, 128))
# image3 = image3.rotate(30, expand=1)
# image.paste(image3, (0, 60), image3)
#
#
# image.show()
#
#
# # im=Image.open("a.jpg")
# #
# # f = ImageFont.load_default()
# # txt=Image.new('L', (500, 50))
# # d = ImageDraw.Draw(txt)
# # d.text( (0, 0), "Someplace Near Boulder",  font=f, fill=255)
# # w=txt.rotate(17.5,  expand=1)
# #
# # im.paste( ImageOps.colorize(w, (0,0,0), (255,128,0)), (0, 460),  w)
# #
# # im.show()
#
# # filename="C:\\Users\\John\\Desktop\\CAR PRIVATE7.docx"
# # doc = Document(filename)
# # list= ['GILBERT SISET']
# # list2 = ['JOHN KAITA']
# # for p in doc.paragraphs:
# #     inline = p.runs
# #     for j in range(0,len(inline)):
# #         for i in range(0, len(list)):
# #             inline[j].text = inline[j].text.replace(list[i], list2[i])
# #             print(p.text)
# #             print(inline[j].text)
# # doc.save('C:\\Users\\John\\Desktop\\CAR PRIVATE7.docx')
#
#
# #
# # def replace_text(content, replacements = dict()):
# #     lines = content.splitlines()
# #
# #     result = ""
# #     in_text = False
# #
# #     for line in lines:
# #         if line == "BT":
# #             in_text = True
# #
# #         elif line == "ET":
# #             in_text = False
# #
# #         elif in_text:
# #             cmd = line[-2:]
# #             if cmd.lower() == 'tj':
# #                 replaced_line = line
# #                 for k, v in replacements.items():
# #                     replaced_line = replaced_line.replace(k, v)
# #                 result += replaced_line + "\n"
# #             else:
# #                 result += line + "\n"
# #             continue
# #
# #         result += line + "\n"
# #
# #     return result
# #
# # def process_data(object, replacements):
# #     data = object.getData()
# #     decoded_data = data.decode('utf-8')
# #
# #     replaced_data = replace_text(decoded_data, replacements)
# #
# #     encoded_data = replaced_data.encode('utf-8')
# #     if object.decodedSelf is not None:
# #         object.decodedSelf.setData(encoded_data)
# #     else:
# #         object.setData(encoded_data)
#
#
# # def docx_replace_regex(doc_obj, regex , replace):
# #
# #     for p in doc_obj.paragraphs:
# #         if regex.search(p.text):
# #             inline = p.runs
# #             # Loop added to work with runs (strings with same style)
# #             for i in range(len(inline)):
# #                 if regex.search(inline[i].text):
# #                     text = regex.sub(replace, inline[i].text)
# #                     inline[i].text = text
# #
# #     for table in doc_obj.tables:
# #         for row in table.rows:
# #             for cell in row.cells:
# #                 docx_replace_regex(cell, regex , replace)
# #
# #
# #
# #
# # filename = "C:\\Users\\John\\Desktop\\CAR PRIVATE7.docx"
# #
# # regex1 = re.compile(r"GILBERT SISET")
# # replace1 = r"JOHN KAITA MABONGA"
# #
# # regex2 = re.compile(r"Love")
# # replace2 = r"Waah"
# #
# # doc = Document(filename)
# #
# # docx_replace_regex(doc, regex1 , replace1)
# # docx_replace_regex(doc, regex2 , replace2)
# #
# #
# # doc.save('C:\\Users\\John\\Desktop\\CAR PRIVATE8.docx')
# #
# # convert("C:\\Users\\John\\Desktop\\CAR PRIVATE7.docx", "C:\\Users\\John\\Desktop\\OUT.pdf")
#
#
#
# def docx_find_replace_text(doc, search_text, replace_text):
#     paragraphs = list(doc.paragraphs)
#     for t in doc.tables:
#         for row in t.rows:
#             for cell in row.cells:
#                 for paragraph in cell.paragraphs:
#                     paragraphs.append(paragraph)
#     for p in paragraphs:
#         if search_text in p.text:
#             inline = p.runs
#             # Replace strings and retain the same style.
#             # The text to be replaced can be split over several runs so
#             # search through, identify which runs need to have text replaced
#             # then replace the text in those identified
#             started = False
#             search_index = 0
#             # found_runs is a list of (inline index, index of match, length of match)
#             found_runs = list()
#             found_all = False
#             replace_done = False
#             for i in range(len(inline)):
#
#                 # case 1: found in single run so short circuit the replace
#                 if search_text in inline[i].text and not started:
#                     found_runs.append((i, inline[i].text.find(search_text), len(search_text)))
#                     text = inline[i].text.replace(search_text, str(replace_text))
#                     inline[i].text = text
#                     replace_done = True
#                     found_all = True
#                     break
#
#                 if search_text[search_index] not in inline[i].text and not started:
#                     # keep looking ...
#                     continue
#
#                 # case 2: search for partial text, find first run
#                 if search_text[search_index] in inline[i].text and inline[i].text[-1] in search_text and not started:
#                     # check sequence
#                     start_index = inline[i].text.find(search_text[search_index])
#                     check_length = len(inline[i].text)
#                     for text_index in range(start_index, check_length):
#                         if inline[i].text[text_index] != search_text[search_index]:
#                             # no match so must be false positive
#                             break
#                     if search_index == 0:
#                         started = True
#                     chars_found = check_length - start_index
#                     search_index += chars_found
#                     found_runs.append((i, start_index, chars_found))
#                     if search_index != len(search_text):
#                         continue
#                     else:
#                         # found all chars in search_text
#                         found_all = True
#                         break
#
#                 # case 2: search for partial text, find subsequent run
#                 if search_text[search_index] in inline[i].text and started and not found_all:
#                     # check sequence
#                     chars_found = 0
#                     check_length = len(inline[i].text)
#                     for text_index in range(0, check_length):
#                         if inline[i].text[text_index] == search_text[search_index]:
#                             search_index += 1
#                             chars_found += 1
#                         else:
#                             break
#                     # no match so must be end
#                     found_runs.append((i, 0, chars_found))
#                     if search_index == len(search_text):
#                         found_all = True
#                         break
#
#             if found_all and not replace_done:
#                 for i, item in enumerate(found_runs):
#                     index, start, length = [t for t in item]
#                     if i == 0:
#                         text = inline[index].text.replace(inline[index].text[start:start + length], str(replace_text))
#                         inline[index].text = text
#                     else:
#                         text = inline[index].text.replace(inline[index].text[start:start + length], '')
#                         inline[index].text = text
#             # print(p.text)
#
#
#
# # sample usage as per example
#
# doc = docx.Document('C:\\Users\\John\\Desktop\\CAR PRIVATE7.docx')
# docx_find_replace_text(doc, 'Love', 'Hope it works ')
# docx_find_replace_text(doc, 'FB15-038216', 'TEST')
# doc.save('C:\\Users\\John\\Desktop\\CAR PRIVATE78888.docx')
#
#
#
#
#
#
#
# single_para = doc.paragraphs[4]
# for run in single_para.runs:
#     print(run.text)
