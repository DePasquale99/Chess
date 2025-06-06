###
###File to generate the single pieces images (hopefully it's not needed again)
###



from PIL import Image 
 
  
img = Image.open("Chess\Game\pieces-3461472050.png") 
 
left = 40
top = 60
right = 1760
bottom = 740
 
  
img_cut = img.crop((left, top, right, bottom)) 
#now the image is 1720x680
#img_cut.show()

black_img = img_cut.crop((0,0,1720,320))

#now the image is 1720x320, 

#I cut each piece into  320 of height and different widths

black_rook = black_img.crop((0,0, 240 ,320))
#black_rook.show()
black_rook.save('Chess\Game\Pieces/black_rook.png')

black_bishop = black_img.crop((275,0, 555,320))
black_bishop.save('Chess\Game\Pieces/black_bishop.png')

black_queen = black_img.crop((570,0, 860 ,320))
black_queen.save('Chess\Game\Pieces/black_queen.png')

black_king = black_img.crop((870,0,1160 ,320))
black_king.save('Chess\Game\Pieces/black_king.png')


black_knight = black_img.crop((1180,0,1450 ,320))
black_knight.save('Chess\Game\Pieces/black_knight.png')

black_pawn = black_img.crop((1515,0, 1715,320))
black_pawn.save('Chess\Game\Pieces/black_pawn.png')

white_img = img_cut.crop((0,360,1720,680))

white_rook = white_img.crop((0,0, 240 ,320))
#white_rook.show()
white_rook.save('Chess\Game\Pieces/white_rook.png')

white_bishop = white_img.crop((275,0, 555,320))
white_bishop.save('Chess\Game\Pieces/white_bishop.png')

white_queen = white_img.crop((570,0, 860 ,320))
white_queen.save('Chess\Game\Pieces/white_queen.png')

white_king = white_img.crop((870,0,1160 ,320))
white_king.save('Chess\Game\Pieces/white_king.png')


white_knight = white_img.crop((1180,0,1450 ,320))
white_knight.save('Chess\Game\Pieces/white_knight.png')

white_pawn = white_img.crop((1515,0, 1715,320))
white_pawn.save('Chess\Game\Pieces/white_pawn.png')