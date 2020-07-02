# Score Function （或许该换个名字）
### 为什么需要 score function
1. 存在检测类型的 Operator， 这类 Operator 接受一张图片，检测出来的会是一组图片，这组图片的个数是不确定的。因此一张图片经过包含检测 Operator 的 Pipeline 的处理，结果是数目不确定的特征向量。
如何在这些向量的最近邻搜索结果结果中筛选出最符合需求的一组结果，需要有特定的打分机制的支持。

2. Phantoscope 0.2.0 之后支持了多 Pipeline 的支持，如何根据多个 field 的搜索结果筛选出最符合需求的一组结果，需要有特定的打分机制的支持。

### score function 分类
1. Inner Field Score Mode

    针对一个 Application 中单个字段中数目不定的几组搜索结果，Phantoscope 提供了 InnerFieldScoreMode 支持个性化的方式筛选最终结果。
    目前支持的几种模式如下所示：(形式为表格？或者单独的章节？)
        
    1. first
    2. avg-select
    3. random-select
    4. distance_first
        
2. Score Mode

    针对一个 Application 中多个字段的搜索结果， Phantoscope 提供了 ScoreMode 支持个性化地组合各个字段的搜索结果，并将最终得分排序选出得分最高的作为最终结果。
    目前支持的几种模式如下所示：
    
    1. first
    2. sum
    3. max
    4. min
    5. multiple
    6. avg

3. Score Function
    
    1. weight
    
        指定特定字段的权重，以改变该字段结果对最终结果的影响。
    
    2. decay functions: 线性
    
        特定字段内搜索结果根据默认排序，衰减对应的得分。目前只实现线性衰减。