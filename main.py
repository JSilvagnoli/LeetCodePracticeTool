import requests

leetcode_url = "https://leetcode.com/graphql"

def getAllQuestions():
    all_questions = []

    limit = 50
    skip = 0

    query = """
    query problemsetQuestionList(
        $categorySlug: String,
        $limit: Int,
        $skip: Int,
        $filters: QuestionListFilterInput
    ) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            totalNum
            data {
                questionFrontendId
                title
                titleSlug
                difficulty
                topicTags {
                    name
                    slug
                }
            }
        }
    }
    """

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referer": "https://leetcode.com/",
        "Origin": "https://leetcode.com",
    }

    while True:
      variables = {
          "categorySlug": "",
          "skip": skip,
          "limit": limit,
          "filters": {}
      }   

      response = requests.post(
          leetcode_url,
          headers=headers,
          json={
              "query": query,
              "variables": variables,
              "operationName": "problemsetQuestionList",
          },
          timeout=30,
      )

      response.raise_for_status()

      result = response.json()

      question_data = result["data"]["problemsetQuestionList"]

      total_num = question_data["totalNum"]
      questions = question_data["data"]

      all_questions.extend(questions)

      skip += limit
      if skip >= total_num:
          break

    return all_questions


def main():
    data = getAllQuestions()
    print(data)


if __name__ == "__main__":
    main()
