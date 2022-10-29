#ifndef SHPP_QUEUE_H
#define SHPP_QUEUE_H
template <typename WorkItem> class SharedPoolProcessorQueue {
    virtual void Put(WorkItem *item) = 0;
    virtual WorkItem* Get() = 0;
    virtual long Qsize() = 0 const;
    virtual bool Empty() = 0 const;
    virtual void Close() = 0;
};
#endif

