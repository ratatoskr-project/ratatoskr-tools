all:
	cd ..; python setup.py install; cd tutorials
	python main.py


markdown:
	jupyter nbconvert *.ipynb --to markdown

jupyter:
	jupyter nbconvert --to notebook --inplace --execute *.ipynb

