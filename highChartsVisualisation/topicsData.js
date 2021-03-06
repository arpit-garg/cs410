/* global window, d3, _
*/

window.getData = (cb) => {
  d3.json('dummy.json', (error, json) => {
    //json = JSON.stringify(json, null, 4)
    let nodes = json
    // nodes.length = 20 // Limiting the set for a quick demo
    nodes = nodes.filter(e => e.year > 0)

    // Sort the nodes by year
    nodes.sort((a, b) => (a.year - b.year))//This may not be needed in our case as the data is time sorted
    const links = []
    let allYears = _.uniq(nodes.map(e => Number(e.year)))
    allYears = allYears.filter(e => isFinite(e))
    allYears = allYears.sort((a, b) => (a - b))
    const leastYear = Math.min.apply(null, allYears)
    const maxYear = Math.max.apply(null, allYears)

    // Creating Year nodes
    /**
     * These year nodes helps us place the actual nodes in time series manner
     * Once the plotting (in DOM) of the actual nodes are done, we will remove these nodes
     */
    const yearNodes = allYears.map((e) => {
      const yearNode = {
        timeSort: `year-${e}`,
        topic: `year-${e}`,
        name: e.toString(),
        year: e,
        topicMilestonePaperLink: '',
        influencedBy: [],
        type: 'year-node',
        cssClasses: [
          'year-node',
        ],
      }
      return yearNode
    })
    yearNodes.forEach((e, idx) => {
      if (idx !== 0) {
        const lastYearNode = yearNodes[idx - 1]
        e.influencedBy.push(lastYearNode.timeSort)
      }
    })

    nodes = [].concat(nodes, yearNodes)
    nodes.forEach((node, nodeIdx) => {
      node.name = node.topic.toString()
      node.cssClasses = node.cssClasses || [`node-${node.timeSort}`]
      node.influencedBy.forEach((originalNodeId, idx) => {
        const sourceIdx = nodes.findIndex(e => e.topic === originalNodeId)
        if(sourceIdx === -1) {
          console.log("Index not found for topic" + originalNodeId)
        }
        console.log(nodes)
        const link = {
          source: sourceIdx,
          target: nodeIdx,
          linkId: `link-${nodeIdx}-${idx}`,
          value: 1, // A dummy value
          cssClasses: [
            'node-link',
            `link-node-id-${node.timeSort}`,
            `link-node-id-${nodes[sourceIdx].timeSort}`,
          ],
        }
        if (node.type === 'year-node') {
          link.cssClasses.push('year-link')
        }

        if(nodes[sourceIdx].hasOwnProperty('cssClasses')) {
          nodes[sourceIdx].cssClasses.push(`node-node-id-${node.timeSort}`)
        }
        else {
         nodes[sourceIdx].cssClasses = [`node-node-id-${node.timeSort}`] 
        }
        node.cssClasses.push(`node-node-id-${nodes[sourceIdx].timeSort}`)

        links.push(link)
      })

      // Connect nodes with prev and next year nodes
      if (node.type !== 'year-node') {
        // Map with previous year node

        const yearIndex = allYears.indexOf(Number(node.year))
        if (yearIndex > 0 && yearIndex !== allYears.length - 1) {
          const prevAvailableYear = allYears[yearIndex - 1]
          const yearNodeIndex = nodes.findIndex(e => e.timeSort === `year-${prevAvailableYear}`)
          // Mapping to the prev year
          links.push({
            source: yearNodeIndex,
            target: nodeIdx,
            linkId: `prev-link-${nodeIdx}-year-${node.year}`,
            type: 'year-link',
            value: 1, // A dummy value
            cssClasses: [
              'year-link',
              `link-node-id-${nodes[yearNodeIndex].timeSort}`,
              `link-node-id-${node.timeSort}`,
            ],
          })
        }

        if (yearIndex < allYears.length - 1 && yearIndex !== -1) {
          // Mapping to next available year
          // Mapping to the prev year
          const nextAvailableYear = allYears[yearIndex + 1]
          const yearNodeIndex = nodes.findIndex(e => e.timeSort === `year-${nextAvailableYear}`)
          links.push({
            source: nodeIdx,
            target: yearNodeIndex,
            linkId: `next-link-year-${node.year}-${nodeIdx}`,
            type: 'year-link',
            value: 1, // A dummy value
            cssClasses: [
              'year-link',
              `link-node-id-${node.id}`,
              `link-node-id-${nodes[yearNodeIndex].timeSort}`,
            ],
          })
        }
      }
    })

    // Preparing another set of year nodes to visualise timeline
    const timeLineLinks = []
    const timeLineNodes = allYears.map((e) => {
      const yearNode = {
        timeSort: `timeline-year-${e}`,
        topic: e.toString(),
        name: e.toString(),
        year: e,
        topicMilestonePaperLink: '',
        influencedBy: [],
        type: 'timeline-node',
        cssClasses: [
          'timeline-node',
        ],
      }
      return yearNode
    })
    timeLineNodes.forEach((e, idx) => {
      if (idx !== 0) {
        const lastYearNode = timeLineNodes[idx - 1]
        e.influencedBy.push(lastYearNode.timeSort)
      }
    })

    timeLineNodes.forEach((node, nodeIdx) => {
      node.name = node.topic.toString()
      node.cssClasses = node.cssClasses || [`time-line-node-${node.timeSort}`]
      node.influencedBy.forEach((originalNodeId, idx) => {
        const sourceIdx = timeLineNodes.findIndex(e => e.timeSort === originalNodeId)
        const link = {
          source: sourceIdx,
          target: nodeIdx,
          linkId: `link-${nodeIdx}-${idx}`,
          value: 1, // A dummy value
          cssClasses: [
            'timeline-link',
            `timeline-link-node-id-${node.timeSort}`,
            `timeline-link-node-id-${timeLineNodes[sourceIdx].timeSort}`,
          ],
        }
        if (node.type === 'year-node') {
          link.cssClasses.push('year-link')
        }

        nodes[sourceIdx].cssClasses.push(`node-node-id-${node.timeSort}`)
        node.cssClasses.push(`node-node-id-${timeLineNodes[sourceIdx].timeSort}`)

        timeLineLinks.push(link)
      })
    })

    cb({
      nodes,
      links,
      timeLineNodes,
      timeLineLinks,
      leastYear,
      maxYear,
      allYears,
    })
  })
}

