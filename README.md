# zip_in_pdf
PDF + ZIP 合并器：把ZIP文件打包至PDF文件中
<p>pdf新文件会自动重命名，如new,new1,new2...</p>
<p>图标文件：<img src="./img/a.ico" alt="image" height="30" width="30" /></p>
<p><img src="./img/1.png" alt="image" height="224" width="419" /><img src="./img/2.png" alt="image" height="223" width="420" /></p>
<p><img src="./img/3.png" alt="image" height="381" width="777" /></p>
<p>&nbsp;</p>
<p><strong><span style="color: #ff0000;">PYTHON直接运行，直接复制下面代码即可</span></strong></p>

<p>&nbsp;</p>
<p><span style="color: #000000;">使用&nbsp;<strong>pyinstaller&nbsp;</strong>打包成单文件时需要添加<strong>&nbsp;hook-tkinterdnd2.py</strong>&nbsp;&nbsp;，与上面代码&nbsp;<strong>run.py&nbsp;</strong>在同级目录即可，<strong>cmd&nbsp;</strong>打包命令如下</span></p>
<pre class="language-python highlighter-hljs"><code>pyinstaller -F -w -n="PDF + ZIP 合并器" --icon=a.ico run.py --additional-hooks-dir=.</code></pre>
<p>&nbsp;</p>
<p><span style="color: #000000;"><strong>hook-tkinterdnd2.py</strong>&nbsp;代码如下</span></p>
<pre class="language-python highlighter-hljs"><code>from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('tkinterdnd2')</code></pre>
<p>&nbsp;</p>
<p><span style="color: #000000;">成品链接<br /> <a  style="color: #ff0000;" rel="noopener" target="_blank" href="./img/PDF + ZIP 合并器.exe">PDF + ZIP 合并器.exe</a> </span></p>
<p>&nbsp;</p>
