# Important Links:

[OverLeaf final report](https://www.overleaf.com/4413719886yyjwcspjcnhw)

# Planning and logs per week

## Week 2

### Meeting notes: 
Discussed which dataset to use. Outcome: use Reddit data

We will have teem meetings every Wednesday after the lecture and every Thursday after our TA meeting. 

#### Decisions:
* Use Python and Flask as back-end
* Front-end to use will be decided base don features we want to visualize
* Use git branching model, where master=stable, all other features are developed in a separate branch. Changes go through a feature review via pull request. 
* Focus on analytics primarily

#### Action items:
Every team member creates 2 paper models of a feature or workflow we want to visualize. Next week we go over the features and discuss any changes


### Idea's from brainstorm session
This list is non-exhaustive. If you have other idea, please add it below or into the board. 

* Visualize how communities evolved over the years -> timeline
* During election cycle, explore relationship between communities
* Sentiment analysis
* Which ones link the most to each other
* Most popular ones
* Visual link explorer -> seo backlinks
* Wordcloud (realtime, get body content and generate)
* (Related) Feature vector analysis: look at the feature vector of a post, find other posts with similar percentages and where they link
* Chain links analysis: how many levels deep
* Echo chamber detection
* Find related subreddits by looking where they link the most
* Thread brigading detection based on sentiment


#### Technical Notes:
The dataset contains post id. The content of the post can be retrieved by the following API call:
https://www.reddit.com/comments/commentIDhere/.json



## Week 3

### Meeting 19/02

* Discussed high level paper prototyping for 2 views
* Discussed architecture of the solution and how we will implement it: use Python (Flask) with Pandas for the data processing. Frontend will be up to the implementation teams per view, including D3 and Bokeh for interactive views. 
* Discussed what to ask Georgi for next day and get initial design approved. 
* Started working on data processing with Pandas to create an API to retrieve the data

## Week 4

### Meeting 26/02

* Make functional prototype by next week
* Visualization design <see image>
* Navigate over time in discreet time intervals on the bottom, support playing animation over time
* Main screen displays graph of interactions between subreddits, where line thickness and color represent different features.
  Optionally the placement of the graph nodes could convey additional information. 
* Hover or click on subreddit shows a radar plot for a given subreddit, showing relationships between these features
* After meeting: continued work on API and started with visualization skeleton first screen


### Team Meeting 27/02
* Finalized static API to return data for frontend and began working on producing results in the backend
* Created frontend skeleton structure with D3.js

## Week 5

### Meeting 05/03

* Prototype looking fine.
* Important to focus on design: colors, user usability/interaction
* Combine the invidual parts of the prototype and design this nicely
* Fix the bar chart with time line soon

## Week 6

### Meeting 11/03

* Progress was fine
* Having a complete demo ready for next week
* Prepare some guidance for the user
* Use an appropiate color scheeme
* Prepare the user stories
* Add feedback actions, like zoom in, hightlight selected nodes etc
* Check the app for possible delays
* Bar charts needs to be refined and integrated
* Final presentation, report and video content was discussed
	* motivations
	* how our vizes are different from a regular graph
	* identify passive elements (e.g. background) and active elements (e.g nodes, seach bar)
	* justify color use, element positions, font used, etc.
	* what are the findings of our vizes
	* what we have archived
	* how components communicate with each other

## Week 7
