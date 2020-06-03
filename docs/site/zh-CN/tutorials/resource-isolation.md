# 资源隔离

在 Phantoscope 中资源是怎么进行隔离的?

在 Phantoscope 中图片资源以 pipeline + encoder 的方式进行隔离

如果两个 application 的 fileds 使用相同的一条 pipeline，那么这两个 application 的这个 fileds 的数据是共通的

如果对 pipeline 进行了更改，那么数据还在吗？

如果仅修改了 processor，数据是不会发生改变的

如果修改了 encoder,那么这个 fileds 对应的数据需要重新上传

旧的数据并不会被删除,只要将 encoder 改回，可以继续使用之前的数据
