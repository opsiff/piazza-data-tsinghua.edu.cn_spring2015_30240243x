# docke-image部署方法

- 1. 下载两个文件'piazza-together_V1.0.0.tar.gz'和解压出'piazza-together_V1.0.0.tar'
- 2. 运行 docker load < piazza-together_V1.0.0.tar
- 3. 执行 docker run -p 8888:80 -d  piazza-together:V1.0.0

注：8888为外网端口 可以修改成80等端口