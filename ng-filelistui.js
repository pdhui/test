(function(window, vx, undefined) {'use strict';

var directive = {};
directive.uiUploadlist = ['$log',
function($log) {		
	return {
		restrict : 'CA',
		compile : function( element, attrs) {	
			var options;
			if(!!attrs.uiUploadlist)
				options = vx.fromJson(attrs.uiUploadlist);
			else
				return;
			var filecontrol = upctrl(element,options);
			function upctrl(element,options){//<li class='completeupload'></li>
				var roottemplate = "<form target='uplist-iframe' name='uplform' enctype='multipart/form-data'  method='post'><div class='uploadpanel' style='display:none'><ul style='overflow:hidden;'><li class='readyupload current'><div class='delfile'><a class='delfilebtn' href='javascript:void(0)'>删除</a></div><span class='uploadfilename'></span></li></ul><a href='javascript:void(0)' id='uplwrapbtnul' class='upla'><span class='btn-text'>上传文件</span><input type='file' name='FILEPATH' class='upload_f'/></a></div><div style='display:none;' id='allhiddenfields' ></div></form>",					
					iframe="<iframe id='uplist-iframe' name='uplist-iframe' src='javascript:false;' style='display:none'></iframe>";
				element.append(vx.element(roottemplate));
				element.closest("[v-page]").append(vx.element(iframe));
			
				return new (function(element,options){
					var uploadwrapper = element.find("#uplwrapbtnul"),
						uploadfilebtn = uploadwrapper.find(".upload_f"),
						uplform = vx.element("form[name='uplform']"),
						iframe = vx.element("#uplist-iframe"),
						rootul = element.find("ul"),
						rootuloffset = rootul.position(),
						curfile="",
						completeupload = "<li class='completeupload'><div class='delfile'><a class='delfilebtn' href='javascript:void(0)'>删除</a></div><span class='uploadfilename'></span></li>",
						readyupload = "<li class='readyupload'><div class='delfile'><a class='delfilebtn' href='javascript:void(0)'>删除</a></div><span class='uploadfilename'></span></li>",
						hiddenfieldswrap = uplform.find("#allhiddenfields"),
						_that = this;
					var action = options.action,
						paramsname = options.paramsname;
					function setForm(form,scope){
						form.innerHTML = "";
						var fields = scope[paramsname];
						for(var key in fields) {
							var input = document.createElement('input');
							input.setAttribute('type', "hidden");
							input.setAttribute('name', key);
							input.setAttribute('value', fields[key]);
							form.appendChild(input);
						};
						//加上会话ID
						var input = document.createElement('input');
						input.setAttribute('name', 'EMP_SID');
						input.setAttribute('value', scope.EMP_SID);
						form.appendChild(input);
						form.setAttribute('action', '/nscf/' +action);
					}
					uploadfilebtn.bind("change",function(e){
						 var filename = vx.element(this).val();
						 if(vx.isEmpty(filename))
							 return;
						 curfile = filename.substr(filename.lastIndexOf("\\")+1);
//						 var params ={
//								 	"OPERTYPE" : "A",
//								 	"BIZNO" : "2014031050963789",
//									"FILENAME" : curfile,
//									"UPLOADERROLE" : "CUST",
//									"UPLOADERNAME" : "待维护",
//									"UPLOADERID" : "2014010650198687"
//								};
						 setForm(hiddenfieldswrap[0],_that.scope);
						 uplform[0].submit();
					 });
					iframe.bind('load',function(event){

						if(iframe.contents().find("body")[0] == undefined) {
							return;
						}
						var response = $(this).contents().find("body")[0].innerText;
						//
						var u = vx.fromJson(response);
						if(!u)
							return;
						if(u.errorCode!="000000"){
//							art.dialog({title:"错误提示！",content:u.errorMessage});
							_that.setText(curfile);
							_that.addReadyBox();
						}else{
//							art.dialog({title:"上传成功",content:"资料上传成功！"});
							
						}
						//
//						iframe.unbind('load');							
					});
					rootul.click(function(e){
						var target = vx.element(e.target);
						if(target.hasClass("delfilebtn"))
						{					
							_that.removeCompletedBox(target[0]);
						}
					});
					this.init = function(){
						this.show();
						rootuloffset = rootul.position();
						this.setFilePos();						
					};
					this.show = function(){
						vx.element(".uploadpanel").show();
					};
					this.setScope = function(scope){
						this.scope = scope;
					};
					this.getReadyBox = function(){
						return element.find("ul .readyupload");
					};
					this.getReadyBoxOffset = function(){
						var rb = this.getReadyBox();
						return rb.position();
					};
					this.setText = function(str){
						rootul.find(".current .uploadfilename").text(str);
					};
					this.setFilePos = function(){
						var readyoffset = this.getReadyBoxOffset(),
							rdbpositionx = readyoffset.left - rootuloffset.left + 18;
						uploadwrapper.css("left",rdbpositionx);
					};
					this.addReadyBox = function(){						
						var currentbox = rootul.find(".current"),readyedbox;
						if(currentbox.length > 0)
						{
							currentbox = vx.element(currentbox[currentbox.length-1]);
							if(currentbox.hasClass("readyupload")){
								currentbox.removeClass("readyupload").addClass("completeupload");
							}							
							readyedbox = vx.element(readyupload);
							currentbox.after(readyedbox);
							currentbox.removeClass("current");						
							
							currentbox.hover(function(e){							
								vx.element(this).find(".delfile").show();
							},function(e){

								vx.element(this).find(".delfile").hide();
							});
						}else{
							readyedbox = vx.element(readyupload);
							rootul.append(readyedbox);							
						}
						readyedbox.addClass("current");
						this.setFilePos();
					};
					this.removeCompletedBox = function(el){
						
						var targetli = vx.element(el).closest("li.completeupload");
						if(targetli.length ==0 )
							return;				
						targetli.remove();
						this.setFilePos();
					};
				})(element,options);
			};
			return {
				post :function(scope, element, attrs) {
					filecontrol.setScope(scope);
					setTimeout(function(){
						filecontrol.init();						
					},0);	
				}
			};
		}
	};
}];
vx.module('ui.libraries').directive(directive);
})(window, window.vx);