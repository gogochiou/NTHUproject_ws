// Generated by gencpp from file mbf_msgs/CheckPointResponse.msg
// DO NOT EDIT!


#ifndef MBF_MSGS_MESSAGE_CHECKPOINTRESPONSE_H
#define MBF_MSGS_MESSAGE_CHECKPOINTRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace mbf_msgs
{
template <class ContainerAllocator>
struct CheckPointResponse_
{
  typedef CheckPointResponse_<ContainerAllocator> Type;

  CheckPointResponse_()
    : state(0)
    , cost(0)  {
    }
  CheckPointResponse_(const ContainerAllocator& _alloc)
    : state(0)
    , cost(0)  {
  (void)_alloc;
    }



   typedef uint8_t _state_type;
  _state_type state;

   typedef uint32_t _cost_type;
  _cost_type cost;



// reducing the odds to have name collisions with Windows.h 
#if defined(_WIN32) && defined(FREE)
  #undef FREE
#endif
#if defined(_WIN32) && defined(INSCRIBED)
  #undef INSCRIBED
#endif
#if defined(_WIN32) && defined(LETHAL)
  #undef LETHAL
#endif
#if defined(_WIN32) && defined(UNKNOWN)
  #undef UNKNOWN
#endif
#if defined(_WIN32) && defined(OUTSIDE)
  #undef OUTSIDE
#endif

  enum {
    FREE = 0u,
    INSCRIBED = 1u,
    LETHAL = 2u,
    UNKNOWN = 3u,
    OUTSIDE = 4u,
  };


  typedef boost::shared_ptr< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> const> ConstPtr;

}; // struct CheckPointResponse_

typedef ::mbf_msgs::CheckPointResponse_<std::allocator<void> > CheckPointResponse;

typedef boost::shared_ptr< ::mbf_msgs::CheckPointResponse > CheckPointResponsePtr;
typedef boost::shared_ptr< ::mbf_msgs::CheckPointResponse const> CheckPointResponseConstPtr;

// constants requiring out of line definition

   

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::mbf_msgs::CheckPointResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::mbf_msgs::CheckPointResponse_<ContainerAllocator1> & lhs, const ::mbf_msgs::CheckPointResponse_<ContainerAllocator2> & rhs)
{
  return lhs.state == rhs.state &&
    lhs.cost == rhs.cost;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::mbf_msgs::CheckPointResponse_<ContainerAllocator1> & lhs, const ::mbf_msgs::CheckPointResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace mbf_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d74139e1f7169aa4fb64b44c3a698692";
  }

  static const char* value(const ::mbf_msgs::CheckPointResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd74139e1f7169aa4ULL;
  static const uint64_t static_value2 = 0xfb64b44c3a698692ULL;
};

template<class ContainerAllocator>
struct DataType< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "mbf_msgs/CheckPointResponse";
  }

  static const char* value(const ::mbf_msgs::CheckPointResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8                      FREE      =  0    # point is in traversable space\n"
"uint8                      INSCRIBED =  1    # point is in inscribed space\n"
"uint8                      LETHAL    =  2    # point is in collision\n"
"uint8                      UNKNOWN   =  3    # point is in unknown space\n"
"uint8                      OUTSIDE   =  4    # point is outside the map\n"
"\n"
"uint8                      state             # point state: FREE, INFLATED, LETHAL, UNKNOWN or OUTSIDE\n"
"uint32                     cost              # cost of the cell at point\n"
"\n"
;
  }

  static const char* value(const ::mbf_msgs::CheckPointResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.state);
      stream.next(m.cost);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct CheckPointResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::mbf_msgs::CheckPointResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::mbf_msgs::CheckPointResponse_<ContainerAllocator>& v)
  {
    s << indent << "state: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.state);
    s << indent << "cost: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.cost);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MBF_MSGS_MESSAGE_CHECKPOINTRESPONSE_H
