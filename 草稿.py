"""
db.getCollection("quora").find({})

use 中大网校
// 根据 answer_id 去重统计总数
db.试题.aggregate([
  {
    $group: {
      _id: "$id"  // 使用字段进行分组
    }
  },
  {
    $count: "totalCount"  // 统计分组后的文档数量
  }
])

// 统计 questionCount 字段总和
db.unique_papers.aggregate([
  {
    $group: {
      _id: null, // 因为我们想要的是所有文档的总和，所以这里使用null作为_id
      total: { $sum: "$questionCount" } // 使用$sum来累加count字段的值
    }
  }
])

db.unique_answers.aggregate([
  {
    $group: {
      _id: "$question_id"  // 使用字段进行分组
    }
  },
  {
    $count: "totalCount"  // 统计分组后的文档数量
  }
])
// 去重到新集合中
db.试题.aggregate([
  {
    $group: {
      _id: "$id",     // 根据 answer_id 进行分组
      doc: { $first: "$$ROOT" }  // 保留每个分组的第一条记录
    }
  },
  {
    $replaceRoot: { newRoot: "$doc" }  // 将结果恢复为原始文档结构
  },
  {
    $out: "unique_questions"  // 将结果输出到新集合 unique_answers
  }
])
// 多字段去重
db.unique_data.aggregate([
  {
    $group: {
      _id: {
        url: "$url",
        answer: "$answer"
      },     // 根据 answer_id 进行分组
      doc: { $first: "$$ROOT" }  // 保留每个分组的第一条记录
    }
  },
  {
    $replaceRoot: { newRoot: "$doc" }  // 将结果恢复为原始文档结构
  },
  {
    $out: "unique_answers"  // 将结果输出到新集合 unique_answers
  }
])
"""
{
  "_id": {
    "$oid": "678e1069f1891382292735b5"
  },
  "biz_app_id": 520947,
  "biz_scenes": 6,
  "qa_biz_params": {
    "search_id": {
      "$numberLong": "1821746588932140"
    },
    "res_id": {
      "$numberLong": "1821746597342283"
    },
    "item_id": 655609361,
    "department": 1,
    "subject": 2,
  }
}