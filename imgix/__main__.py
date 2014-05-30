import imgix 
if __name__ == "__main__":
	builder = imgix.UrlBuilder("static.imgix.net", sign_key="sda2345")
	print builder.create_url("/treefrog.jpg?testing/", w=10, h=400, fit="crop")
