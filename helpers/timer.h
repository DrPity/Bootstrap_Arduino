//----Wait function to reset timers---------------------------------------------

void wait(long _waitTime, long _numberOfIndex)
{
  waitTime[_numberOfIndex] = _waitTime;
  currentTime[_numberOfIndex] = millis();
}

//----Check if a timer runs out-------------------------------------------------

bool checkTimers(int _index)
{
  if(millis() - currentTime[_index] >= waitTime[_index]){
    currentTime[_index] = millis();
    return true;
  }else
  {
    return false;
  }
}
